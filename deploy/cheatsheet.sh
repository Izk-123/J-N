#!/bin/bash
# ================================================================
#  J&N Building Products — Server Management Cheatsheet
#  Save this! These are the most useful commands on the server.
# ================================================================

# ── SERVICE CONTROL ───────────────────────────────────────────────
systemctl status jandn                    # Is Gunicorn running?
systemctl restart jandn                   # Restart app (after code changes)
systemctl stop jandn                      # Stop app
systemctl start jandn                     # Start app

# ── LOGS (most useful for debugging) ─────────────────────────────
journalctl -u jandn -f                    # Live Gunicorn logs
journalctl -u jandn --since "1 hour ago"  # Last hour of logs
tail -f /var/log/jandn/gunicorn.error.log # Gunicorn error log
tail -f /var/log/nginx/jandn.mw.error.log # Nginx error log
tail -f /var/log/nginx/jandn.mw.access.log # Who visited the site

# ── DJANGO MANAGEMENT ─────────────────────────────────────────────
cd /var/www/jandn

# Create admin user
venv/bin/python manage.py createsuperuser \
    --settings=jn_building_products.settings_production

# Apply DB changes after a model update
venv/bin/python manage.py makemigrations \
    --settings=jn_building_products.settings_production
venv/bin/python manage.py migrate \
    --settings=jn_building_products.settings_production

# Rebuild static files (after CSS/JS/image changes)
venv/bin/python manage.py collectstatic \
    --settings=jn_building_products.settings_production --noinput

# Django shell (for database queries)
venv/bin/python manage.py shell \
    --settings=jn_building_products.settings_production

# Check for errors
venv/bin/python manage.py check \
    --settings=jn_building_products.settings_production

# ── NGINX ─────────────────────────────────────────────────────────
nginx -t                                  # Test Nginx config
systemctl reload nginx                    # Reload after config change
systemctl restart nginx                   # Full restart

# ── SSL CERTIFICATE ───────────────────────────────────────────────
certbot renew --dry-run                   # Test SSL auto-renewal
certbot renew                             # Force renewal
certbot certificates                      # List certs + expiry dates

# Manual SSL install (if DNS wasn't ready during first deploy):
certbot --nginx -d jandn.mw -d www.jandn.mw

# ── DATABASE ──────────────────────────────────────────────────────
# Backup database
cp /var/www/jandn/db.sqlite3 /root/db_backup_$(date +%Y%m%d).sqlite3

# View enquiries directly
sqlite3 /var/www/jandn/db.sqlite3 \
    "SELECT name, phone, status, datetime(created_at,'localtime') FROM contacts_contactmessage ORDER BY created_at DESC LIMIT 20;"

# ── ENVIRONMENT VARIABLES ─────────────────────────────────────────
nano /var/www/jandn/.env                  # Edit env vars
systemctl restart jandn                   # Always restart after editing .env

# ── DISK & MEMORY ─────────────────────────────────────────────────
df -h                                     # Disk usage
free -h                                   # Memory usage
du -sh /var/www/jandn/media/              # Size of uploaded images

# ── UPDATES (when you change code locally) ────────────────────────
# 1. On your local machine: zip the project and SCP it up
scp jn_building_products_phase3.zip root@204.168.251.91:/root/

# 2. On the server: run the update script
bash /var/www/jandn/deploy/update.sh
