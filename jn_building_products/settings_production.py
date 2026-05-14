"""
Production settings for J&N Building Products — VPS Deployment
Domain: jandn.mw | Server: 204.168.251.91
PostgreSQL + cPanel email
"""
from .settings import *
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = False

ALLOWED_HOSTS = [
    'jandn.mw',
    'www.jandn.mw',
    '204.168.251.91',
    'localhost',
    '127.0.0.1',
]

# Add trusted origins for CSRF (required for POST requests over HTTPS)
CSRF_TRUSTED_ORIGINS = [
    'https://jandn.mw',
    'https://www.jandn.mw',
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Database – PostgreSQL (credentials from .env)
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

# Static & Media – served by Nginx
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise middleware (fallback)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Email – cPanel (or your mail server)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.jandn.mw'          # or your SMTP host
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'info@jandn.mw')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = f'J&N Building Products <{EMAIL_HOST_USER}>'
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@jandn.mw')

# Security headers (activate after SSL)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# SSL / HTTPS settings – enabled only when HTTPS_ENABLED=true in .env
# SSL / HTTPS settings – enabled only when HTTPS_ENABLED=true in .env
if os.environ.get('HTTPS_ENABLED', '').lower() == 'true':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow WebSocket handshake to include session cookie
    SESSION_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_SAMESITE = 'None'

# Create logs directory automatically
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)
    
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Logging (optional)
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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240   # default is 1000
DATA_UPLOAD_MAX_NUMBER_FILES = 100      # default is 100
