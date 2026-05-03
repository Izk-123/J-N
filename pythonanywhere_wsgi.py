"""
WSGI config for PythonAnywhere deployment.

INSTRUCTIONS:
  1. In PythonAnywhere dashboard → Web → WSGI configuration file
  2. Replace the entire file contents with this file's contents
  3. Change 'yourusername' to your actual PythonAnywhere username
  4. Click "Reload" in the Web tab
"""

import sys
import os

# ── 1. Add your project to the Python path ────────────────────────────────────
# Replace 'yourusername' with your PythonAnywhere username
path = '/home/yourusername/jn_building_products'
if path not in sys.path:
    sys.path.insert(0, path)

# ── 2. Set environment variables ──────────────────────────────────────────────
os.environ['DJANGO_SETTINGS_MODULE'] = 'jn_building_products.settings_production'

# Optional: set secret key as environment variable (more secure)
# os.environ['DJANGO_SECRET_KEY'] = 'your-very-long-random-secret-key-here'
# os.environ['EMAIL_HOST_USER'] = 'your@gmail.com'
# os.environ['EMAIL_HOST_PASSWORD'] = 'your-gmail-app-password'

# ── 3. Activate virtual environment ───────────────────────────────────────────
# Replace 'yourusername' and Python version (3.10, 3.11, etc.) as needed
activate_this = '/home/yourusername/.virtualenvs/jnenv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# ── 4. Start the Django WSGI application ─────────────────────────────────────
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
