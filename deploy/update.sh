#!/bin/bash
# ================================================================
#  J&N Building Products — Update Script
#  Run this whenever you make code changes and re-upload
#  Usage: bash update.sh
# ================================================================
set -e

APP_DIR="/var/www/jandn"
SERVICE_NAME="jandn"
UPLOAD_ZIP="/root/jn_building_products_phase3.zip"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
info() { echo -e "  ${YELLOW}→${NC} $1"; }

echo -e "\n${BLUE}${BOLD}  J&N — Applying Updates${NC}\n"

cd "$APP_DIR"
export $(grep -v '^#' .env | xargs)

# If a new ZIP was uploaded, extract it (preserving .env, media, db)
if [ -f "$UPLOAD_ZIP" ]; then
    info "New ZIP found — extracting code files..."
    unzip -q -o "$UPLOAD_ZIP" -d /tmp/jandn_update
    SRC=$([ -d "/tmp/jandn_update/jn_building_products" ] && echo "/tmp/jandn_update/jn_building_products" || echo "/tmp/jandn_update")

    # Copy everything EXCEPT .env, db, media (preserve those)
    rsync -a --exclude='.env' --exclude='db.sqlite3' --exclude='media/' \
          "$SRC/" "$APP_DIR/"
    rm -rf /tmp/jandn_update
    rm "$UPLOAD_ZIP"
    ok "Code files updated"
fi

info "Installing any new packages..."
"$APP_DIR/venv/bin/pip" install -r requirements.txt -q

info "Running migrations..."
"$APP_DIR/venv/bin/python" manage.py migrate \
    --settings=jn_building_products.settings_production --noinput

info "Collecting static files..."
"$APP_DIR/venv/bin/python" manage.py collectstatic \
    --settings=jn_building_products.settings_production --noinput -v 0

info "Fixing permissions..."
chown -R www-data:www-data "$APP_DIR"
chmod 600 "$APP_DIR/.env"

info "Restarting Gunicorn..."
systemctl restart "$SERVICE_NAME"
sleep 2

systemctl is-active --quiet "$SERVICE_NAME" && \
    ok "Site updated and running! ✨" || \
    echo "  ⚠ Gunicorn may have issues — check: journalctl -u $SERVICE_NAME"

echo ""
echo -e "  🌐 ${GREEN}https://jandn.mw${NC}"
echo ""
