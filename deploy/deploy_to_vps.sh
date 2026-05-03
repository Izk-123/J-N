#!/bin/bash
# ================================================================
#  J&N Building Products — VPS Deployment Script
#  Server: 204.168.251.91  |  Domain: jandn.mw
#  Run as root: bash deploy_to_vps.sh
# ================================================================
set -e  # Exit immediately on any error

DOMAIN="jandn.mw"
APP_DIR="/var/www/jandn"
REPO_ZIP="/root/jn_building_products_phase3.zip"
SERVICE_NAME="jandn"
NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"
LOG_DIR="/var/log/jandn"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

banner() { echo -e "\n${BLUE}${BOLD}══════════════════════════════════════════${NC}"; echo -e "${BLUE}${BOLD}  $1${NC}"; echo -e "${BLUE}${BOLD}══════════════════════════════════════════${NC}"; }
ok()     { echo -e "  ${GREEN}✓${NC} $1"; }
info()   { echo -e "  ${YELLOW}→${NC} $1"; }
err()    { echo -e "  ${RED}✗ ERROR:${NC} $1"; exit 1; }

clear
echo -e "${BOLD}"
cat << 'LOGO'
     _ ___     _   _   ___      _ _    _ _
    | |_  )   | \ | | | _ )_  _(_) |__| (_)_ _  __ _
 _  | |/ /    |  \| | | _ \ || | | / _` | | ' \/ _` |
 \__/ /___| __|_|\__| |___/\_,_|_|_\__,_|_|_||_\__, |
           |___|                                 |___/
     Make Your House Smile — VPS Deployment v1.0
LOGO
echo -e "${NC}"
echo -e "  Domain : ${GREEN}$DOMAIN${NC}"
echo -e "  Server : ${GREEN}204.168.251.91${NC}"
echo -e "  Target : ${GREEN}$APP_DIR${NC}"
echo ""

# ── STEP 1: System packages ───────────────────────────────────────────────────
banner "Step 1/9 — Installing system packages"
info "Updating apt..."
apt-get update -qq
info "Installing Nginx, Python, Certbot, unzip..."
apt-get install -y -qq \
    nginx python3 python3-pip python3-venv python3-dev \
    certbot python3-certbot-nginx \
    unzip git curl ufw sqlite3
ok "System packages installed"

# ── STEP 2: Firewall ──────────────────────────────────────────────────────────
banner "Step 2/9 — Configuring firewall"
ufw --force reset > /dev/null
ufw default deny incoming > /dev/null
ufw default allow outgoing > /dev/null
ufw allow ssh > /dev/null
ufw allow 'Nginx Full' > /dev/null
ufw --force enable > /dev/null
ok "Firewall: SSH + HTTP + HTTPS open"

# ── STEP 3: Deploy app files ──────────────────────────────────────────────────
banner "Step 3/9 — Deploying application files"

# Create app directory
mkdir -p "$APP_DIR"
mkdir -p "$LOG_DIR"

# Unzip project
if [ -f "$REPO_ZIP" ]; then
    info "Extracting project from ZIP..."
    unzip -q -o "$REPO_ZIP" -d /tmp/jandn_extract
    # Handle nested folder in zip
    if [ -d "/tmp/jandn_extract/jn_building_products" ]; then
        cp -r /tmp/jandn_extract/jn_building_products/. "$APP_DIR/"
    else
        cp -r /tmp/jandn_extract/. "$APP_DIR/"
    fi
    rm -rf /tmp/jandn_extract
    ok "Project files extracted to $APP_DIR"
else
    err "ZIP file not found at $REPO_ZIP. Upload it first:\n  scp jn_building_products_phase3.zip root@204.168.251.91:/root/"
fi

# ── STEP 4: Python virtual environment ───────────────────────────────────────
banner "Step 4/9 — Setting up Python environment"
info "Creating virtual environment..."
python3 -m venv "$APP_DIR/venv"
info "Installing Python packages..."
"$APP_DIR/venv/bin/pip" install --upgrade pip -q
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -q
ok "Virtual environment ready"

# ── STEP 5: Environment file ──────────────────────────────────────────────────
banner "Step 5/9 — Creating environment file"
if [ ! -f "$APP_DIR/.env" ]; then
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits + '!@#%^&*(-_=+)') for _ in range(64)))")

    cat > "$APP_DIR/.env" << ENVEOF
DJANGO_SETTINGS_MODULE=jn_building_products.settings_production
DJANGO_SECRET_KEY=$SECRET_KEY
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
ADMIN_EMAIL=
HTTPS_ENABLED=false
ENVEOF
    chmod 600 "$APP_DIR/.env"
    ok "Environment file created (secret key auto-generated)"
    echo -e "  ${YELLOW}⚠  Edit /var/www/jandn/.env to add your Gmail credentials${NC}"
else
    ok "Environment file already exists — skipping"
fi

# ── STEP 6: Django setup ──────────────────────────────────────────────────────
banner "Step 6/9 — Running Django setup"

cd "$APP_DIR"
export $(grep -v '^#' .env | xargs)

info "Running database migrations..."
"$APP_DIR/venv/bin/python" manage.py migrate --settings=jn_building_products.settings_production --noinput

info "Collecting static files..."
"$APP_DIR/venv/bin/python" manage.py collectstatic --settings=jn_building_products.settings_production --noinput -v 0

info "Loading sample data..."
"$APP_DIR/venv/bin/python" manage.py load_sample_data --settings=jn_building_products.settings_production 2>/dev/null || true

ok "Django setup complete"

# ── STEP 7: File permissions ───────────────────────────────────────────────────
banner "Step 7/9 — Setting file permissions"
chown -R www-data:www-data "$APP_DIR"
chown -R www-data:www-data "$LOG_DIR"
chmod -R 755 "$APP_DIR"
chmod 600 "$APP_DIR/.env"
chmod -R 775 "$APP_DIR/media"
chmod -R 755 "$APP_DIR/staticfiles"
ok "Permissions set"

# ── STEP 8: Nginx configuration ───────────────────────────────────────────────
banner "Step 8/9 — Configuring Nginx (HTTP first, HTTPS after SSL)"

# Write HTTP-only nginx config (will be upgraded to HTTPS by Certbot)
cat > "$NGINX_CONF" << NGINXEOF
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;

    access_log /var/log/nginx/${DOMAIN}.access.log;
    error_log  /var/log/nginx/${DOMAIN}.error.log;

    client_max_body_size 20M;

    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/media/;
        expires 7d;
    }

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host \$host;
        proxy_set_header   X-Real-IP \$remote_addr;
        proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout    60s;
    }
}
NGINXEOF

# Enable site
ln -sf "$NGINX_CONF" "/etc/nginx/sites-enabled/$DOMAIN"
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t && systemctl reload nginx
ok "Nginx configured and running"

# ── STEP 9: Gunicorn systemd service ──────────────────────────────────────────
banner "Step 9/9 — Setting up Gunicorn service"

cat > "/etc/systemd/system/$SERVICE_NAME.service" << SVCEOF
[Unit]
Description=J&N Building Products — Gunicorn
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind 127.0.0.1:8000 \\
    --timeout 120 \\
    --access-logfile $LOG_DIR/gunicorn.access.log \\
    --error-logfile $LOG_DIR/gunicorn.error.log \\
    jn_building_products.wsgi:application
EnvironmentFile=$APP_DIR/.env
Restart=on-failure
RestartSec=5s
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl is-active --quiet "$SERVICE_NAME" && ok "Gunicorn service started" || err "Gunicorn failed to start. Check: journalctl -u $SERVICE_NAME"

# ── SSL Certificate ────────────────────────────────────────────────────────────
banner "🔒 Installing SSL Certificate (Let's Encrypt)"
info "Requesting certificate for $DOMAIN and www.$DOMAIN..."
certbot --nginx \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" \
    --non-interactive \
    --agree-tos \
    --register-unsafely-without-email \
    --redirect 2>&1 | tail -5 && {

    # Enable HTTPS in Django
    sed -i 's/HTTPS_ENABLED=false/HTTPS_ENABLED=true/' "$APP_DIR/.env"
    systemctl restart "$SERVICE_NAME"
    ok "SSL certificate installed! HTTPS is live."
} || {
    echo -e "  ${YELLOW}⚠  SSL failed (DNS may not be pointed yet). Site works over HTTP.${NC}"
    echo -e "  ${YELLOW}   Point jandn.mw to 204.168.251.91, then run:${NC}"
    echo -e "  ${YELLOW}   certbot --nginx -d jandn.mw -d www.jandn.mw${NC}"
}

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}"
cat << 'DONE'
╔══════════════════════════════════════════════════════╗
║   ✅  J&N Building Products is DEPLOYED!             ║
╚══════════════════════════════════════════════════════╝
DONE
echo -e "${NC}"
echo -e "  🌐 Website:   ${GREEN}http://jandn.mw${NC} (or https:// if SSL worked)"
echo -e "  🔐 Admin:     ${GREEN}http://jandn.mw/admin/${NC}"
echo -e "  📊 Dashboard: ${GREEN}http://jandn.mw/dashboard/${NC}"
echo ""
echo -e "${YELLOW}${BOLD}  NEXT STEPS:${NC}"
echo -e "  1. Create admin user:  ${BOLD}cd /var/www/jandn && venv/bin/python manage.py createsuperuser --settings=jn_building_products.settings_production${NC}"
echo -e "  2. Edit email config:  ${BOLD}nano /var/www/jandn/.env${NC}"
echo -e "  3. Restart after edit: ${BOLD}systemctl restart jandn${NC}"
echo -e "  4. Check logs:         ${BOLD}journalctl -u jandn -f${NC}"
echo -e "  5. Nginx logs:         ${BOLD}tail -f /var/log/nginx/jandn.mw.error.log${NC}"
echo ""
echo -e "  ${BOLD}Point your domain DNS:${NC}"
echo -e "  A record:  jandn.mw      → 204.168.251.91"
echo -e "  A record:  www.jandn.mw  → 204.168.251.91"
echo ""
