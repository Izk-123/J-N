"""
Production settings for J&N Building Products — VPS Deployment
Domain: jandn.mw | Server: 204.168.251.91
PostgreSQL + cPanel email
"""
from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'jandn.mw',
    'www.jandn.mw',
    '204.168.251.91',
    'localhost',
    '127.0.0.1',
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# PostgreSQL database (credentials via environment variables)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'jandn_db'),
        'USER': os.environ.get('DB_USER', 'jandn_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static & Media — Nginx serves these directly in production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise fallback (Nginx handles static/media if correctly configured,
# but WhiteNoise ensures they work even without Nginx for static)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# cPanel Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.jandn.mw'        # cPanel mail server (or the server hostname)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'info@jandn.mw')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = f'J&N Building Products <{EMAIL_HOST_USER}>'
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@jandn.mw')

# Security headers (activate after SSL is live)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = os.environ.get('HTTPS_ENABLED', '') == 'true'
SESSION_COOKIE_SECURE = os.environ.get('HTTPS_ENABLED', '') == 'true'
CSRF_COOKIE_SECURE = os.environ.get('HTTPS_ENABLED', '') == 'true'

# Logging (optional but helpful)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
