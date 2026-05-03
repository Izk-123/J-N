#!/bin/bash
# ============================================================
# J&N Building Products - One-Command Setup Script
# ============================================================
# Usage: chmod +x setup.sh && ./setup.sh

echo ""
echo "====================================================="
echo "  J&N Building Products - Project Setup"
echo "====================================================="
echo ""

# 1. Create virtual environment
echo "[1/6] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "[2/6] Installing dependencies..."
pip install -r requirements.txt --quiet

# 3. Make migrations
echo "[3/6] Creating database migrations..."
python manage.py makemigrations core products services projects gallery contacts

# 4. Apply migrations
echo "[4/6] Applying migrations..."
python manage.py migrate

# 5. Collect static files
echo "[5/6] Collecting static files..."
python manage.py collectstatic --noinput --verbosity 0

# 6. Create superuser prompt
echo "[6/6] Creating admin user..."
echo ""
echo "Please create your admin login:"
python manage.py createsuperuser

echo ""
echo "====================================================="
echo "  ✅  Setup Complete!"
echo "====================================================="
echo ""
echo "  To start the server:"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Then open: http://127.0.0.1:8000"
echo "  Admin panel: http://127.0.0.1:8000/admin"
echo ""
echo "  FIRST STEPS in admin:"
echo "  1. Go to 'Site Settings' and fill in your company info"
echo "  2. Add product categories"
echo "  3. Add your products with images"
echo "  4. Add services"
echo "  5. Add completed projects"
echo ""
