#!/bin/bash
# =============================================================================
# J&N Building Products – Full Deployment Script for Ubuntu VPS
# Domain: jandn.mw | Server IP: 204.168.251.91
# =============================================================================

set -e  # Exit on any error

echo "====================================================="
echo "Deploying J&N Building Products to VPS"
echo "====================================================="

# -----------------------------------------------------------------------------
# 1. Update system and install system dependencies
# -----------------------------------------------------------------------------
echo "Step 1: Installing system packages..."
sudo apt update
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib \
                    redis-server git curl certbot python3-certbot-nginx

# -----------------------------------------------------------------------------
# 2. Clone the repository (or update if existing)
# -----------------------------------------------------------------------------
cd /home/project
if [ -d "jn_building_products" ]; then
    echo "Project directory exists. Pulling latest changes..."
    cd jn_building_products
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/Izk-123/J-N.git jn_building_products
    cd jn_building_products
fi

# -----------------------------------------------------------------------------
# 3. Set up Python virtual environment and install dependencies
# -----------------------------------------------------------------------------
echo "Step 3: Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install django gunicorn daphne channels channels-redis redis psycopg2-binary \
            whitenoise python-decouple pillow django-htmx django-unfold

# If requirements.txt exists, use it
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# -----------------------------------------------------------------------------
# 4. Create .env file from template (interactive)
# -----------------------------------------------------------------------------
if [ ! -f ".env" ]; then
    echo "Step 4: Creating .env file. Please provide values:"
    read -p "DJANGO_SECRET_KEY (generate a random one): " secret_key
    read -p "DB_NAME (default jandn_db): " db_name
    read -p "DB_USER (default jandn_user): " db_user
    read -sp "DB_PASSWORD: " db_password
    echo ""
    read -p "EMAIL_HOST_USER (info@jandn.mw): " email_user
    read -sp "EMAIL_HOST_PASSWORD: " email_pass
    echo ""

    cat > .env <<EOF
DJANGO_SECRET_KEY=${secret_key:-$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")}
DEBUG=False
ALLOWED_HOSTS=jandn.mw,www.jandn.mw,204.168.251.91,localhost,127.0.0.1
DB_NAME=${db_name:-jandn_db}
DB_USER=${db_user:-jandn_user}
DB_PASSWORD=${db_password:-StrongPassword123!}
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=${email_user:-info@jandn.mw}
EMAIL_HOST_PASSWORD=${email_pass}
ADMIN_EMAIL=admin@jandn.mw
HTTPS_ENABLED=false
EOF
    echo ".env file created."
else
    echo ".env already exists. Skipping."
fi

# -----------------------------------------------------------------------------
# 5. Create PostgreSQL database and user
# -----------------------------------------------------------------------------
echo "Step 5: Setting up PostgreSQL..."
sudo -u postgres psql <<EOF
DROP DATABASE IF EXISTS jandn_db;
DROP USER IF EXISTS jandn_user;
CREATE USER jandn_user WITH PASSWORD '${db_password:-StrongPassword123!}';
CREATE DATABASE jandn_db OWNER jandn_user;
ALTER ROLE jandn_user SET client_encoding TO 'utf8';
ALTER USER jandn_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE jandn_db TO jandn_user;
EOF

# -----------------------------------------------------------------------------
# 6. Run migrations, collect static, create superuser
# -----------------------------------------------------------------------------
echo "Step 6: Running Django migrations and collecting static..."
python manage.py makemigrations --settings=jn_building_products.settings_production
python manage.py migrate --settings=jn_building_products.settings_production
python manage.py collectstatic --noinput --settings=jn_building_products.settings_production

echo "Creating superuser (interactive)..."
python manage.py createsuperuser --settings=jn_building_products.settings_production

# -----------------------------------------------------------------------------
# 7. Create systemd service for Daphne (ASGI with Channels)
# -----------------------------------------------------------------------------
echo "Step 7: Setting up Daphne systemd service..."
sudo tee /etc/systemd/system/daphne-jn.service > /dev/null <<EOF
[Unit]
Description=Daphne ASGI for J&N Building Products (Channels)
After=network.target redis-server.service

[Service]
User=root
Group=root
WorkingDirectory=/home/project/jn_building_products
Environment="PATH=/home/project/jn_building_products/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=jn_building_products.settings_production"
EnvironmentFile=/home/project/jn_building_products/.env
ExecStart=/home/project/jn_building_products/venv/bin/daphne -b 127.0.0.1 -p 8001 jn_building_products.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable daphne-jn
sudo systemctl restart daphne-jn

# -----------------------------------------------------------------------------
# 8. Configure Nginx (HTTP only, SSL will be added by Certbot)
# -----------------------------------------------------------------------------
echo "Step 8: Configuring Nginx..."
sudo tee /etc/nginx/sites-available/jandn > /dev/null <<EOF
server {
    listen 80;
    server_name jandn.mw www.jandn.mw;

    location /static/ {
        alias /home/project/jn_building_products/staticfiles/;
    }

    location /media/ {
        alias /home/project/jn_building_products/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/jandn /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# -----------------------------------------------------------------------------
# 9. Obtain SSL certificate (if domain resolves)
# -----------------------------------------------------------------------------
echo "Step 9: Attempting SSL certificate (ensure DNS points to this VPS)..."
if sudo certbot --nginx -d jandn.mw -d www.jandn.mw --non-interactive --agree-tos --email admin@jandn.mw; then
    echo "SSL certificate obtained. Set HTTPS_ENABLED=true in .env"
    sed -i 's/HTTPS_ENABLED=false/HTTPS_ENABLED=true/' .env
    sudo systemctl restart daphne-jn
    sudo systemctl reload nginx
else
    echo "Certbot failed – DNS may not be propagated yet. Run manually later:"
    echo "  sudo certbot --nginx -d jandn.mw -d www.jandn.mw"
    echo "  Then set HTTPS_ENABLED=true in .env and restart daphne."
fi

# -----------------------------------------------------------------------------
# 10. Final status and info
# -----------------------------------------------------------------------------
echo "====================================================="
echo "Deployment completed!"
echo "Check service status:"
sudo systemctl status daphne-jn --no-pager
echo "Nginx status:"
sudo systemctl status nginx --no-pager
echo "====================================================="
echo "Visit: https://jandn.mw (once DNS/SSL ready)"
echo "Admin: https://jandn.mw/admin"
echo "Logs: sudo journalctl -u daphne-jn -f"
echo "====================================================="