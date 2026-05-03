"""
Production settings for J&N Building Products — VPS Deployment
Domain: jandn.mw | Server: 204.168.251.91
"""
from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'jandn.mw',
    'www.jandn.mw',
    '204.168.251.91',
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static & Media — Nginx serves these directly
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise fallback
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Email notifications
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'J&N Building Products <noreply@jandn.mw>'
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', '')

# Security headers (activated after SSL is live)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = os.environ.get('HTTPS_ENABLED', '') == 'true'
SESSION_COOKIE_SECURE = os.environ.get('HTTPS_ENABLED', '') == 'true'
CSRF_COOKIE_SECURE = os.environ.get('HTTPS_ENABLED', '') == 'true'
