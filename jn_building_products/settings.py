import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-change-this-in-production-jnbuildingproducts2024'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Unfold MUST come before django.contrib.admin
    'daphne',
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.simple_history',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # HTMX
    'django_htmx',

    # Local apps
    'core',
    'products',
    'services',
    'projects',
    'gallery',
    'contacts',
    'construction',
    'mining',
    'timber',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_htmx.middleware.HtmxMiddleware',   # HTMX middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.VisitorTrackingMiddleware', 
]

ROOT_URLCONF = 'jn_building_products.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'jn_building_products.wsgi.application'
ASGI_APPLICATION = 'jn_building_products.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Redis in production
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Blantyre'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── UNFOLD ADMIN CONFIGURATION ─────────────────────────────────────────────
from django.templatetags.static import static
from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "J&N Admin",
    "SITE_HEADER": "J&N Building Products",
    "SITE_SUBHEADER": "Make Your House Smile",
    "SITE_URL": "/",
    "SITE_LOGO": lambda request: static("images/logo.png"),
    "SITE_LOGO_COLLAPSED": lambda request: static("images/logo.png"),
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "32x32", "type": "image/png", "href": lambda request: static("images/logo.png")},
    ],
    "DASHBOARD_CALLBACK": "core.dashboard.dashboard_callback",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": "Development" if DEBUG else "Production",
    "COLORS": {
        "primary": {
            "50":  "255 245 245",
            "100": "255 228 228",
            "200": "255 196 196",
            "300": "255 153 153",
            "400": "255 102 102",
            "500": "214 40 40",
            "600": "180 28 28",
            "700": "150 20 20",
            "800": "120 15 15",
            "900": "90 10 10",
            "950": "60 5 5",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            # ── Dashboard ──
            {
                "title": "Dashboard",
                "separator": False,
                "items": [
                    {
                        "title": "Overview",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "View Website",
                        "icon": "open_in_new",
                        "link": "/",
                        "target": "_blank",
                    },
                ],
            },
            # ── Enquiries ──
            {
                "title": "Enquiries",
                "separator": True,
                "items": [
                    {
                        "title": "Contact Messages",
                        "icon": "mail",
                        "link": reverse_lazy("admin:contacts_contactmessage_changelist"),
                        "badge": "core.admin_badges.new_messages",
                    },
                ],
            },
            # ── Building Products (was "Catalogue") ──
            {
                "title": "Building Products",
                "separator": True,
                "items": [
                    {
                        "title": "Products",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:products_product_changelist"),
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:products_category_changelist"),
                    },
                    {
                        "title": "Building Settings",
                        "icon": "settings",
                        "link": reverse_lazy("admin:products_buildingsettings_change", args=[1]),
                    },
                ],
            },
            # ── Construction Co. ──
            {
                "title": "🏗️ Construction Co.",
                "separator": True,
                "items": [
                    {
                        "title": "Site Config",
                        "icon": "tune",
                        "link": reverse_lazy("admin:construction_constructionconfig_changelist"),
                    },
                    {
                        "title": "Services",
                        "icon": "handyman",
                        "link": reverse_lazy("admin:construction_constructionservice_changelist"),
                    },
                    {
                        "title": "Projects",
                        "icon": "apartment",
                        "link": reverse_lazy("admin:construction_constructionproject_changelist"),
                    },
                    {
                        "title": "Team",
                        "icon": "groups",
                        "link": reverse_lazy("admin:construction_teammember_changelist"),
                    },
                ],
            },
            # ── Mining Co. ──
            {
                "title": "⛏️ Mining Co.",
                "separator": True,
                "items": [
                    {
                        "title": "Site Config",
                        "icon": "tune",
                        "link": reverse_lazy("admin:mining_miningconfig_changelist"),
                    },
                    {
                        "title": "Minerals",
                        "icon": "diamond",
                        "link": reverse_lazy("admin:mining_mineralproduct_changelist"),
                    },
                    {
                        "title": "Operations",
                        "icon": "terrain",
                        "link": reverse_lazy("admin:mining_miningoperation_changelist"),
                    },
                    {
                        "title": "Equipment",
                        "icon": "precision_manufacturing",
                        "link": reverse_lazy("admin:mining_miningequipment_changelist"),
                    },
                ],
            },
            # ── Timber Co. ──
            {
                "title": "🌲 Timber Co.",
                "separator": True,
                "items": [
                    {
                        "title": "Site Config",
                        "icon": "tune",
                        "link": reverse_lazy("admin:timber_timbersettings_changelist"),
                    },
                    {
                        "title": "Timber Products",
                        "icon": "forest",
                        "link": reverse_lazy("admin:timber_timberproduct_changelist"),
                    },
                    {
                        "title": "Timber Projects",
                        "icon": "landscape",
                        "link": reverse_lazy("admin:timber_timberproject_changelist"),
                    },
                ],
            },
            # ── Media (Gallery) – remove if not needed ──
            {
                "title": "Media",
                "separator": True,
                "items": [
                    {
                        "title": "Gallery",
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:gallery_galleryimage_changelist"),
                    },
                ],
            },
            # ── Group / Website settings ──
            {
                "title": "Group",
                "separator": True,
                "items": [
                    {
                        "title": "Group Config",
                        "icon": "corporate_fare",
                        "link": reverse_lazy("admin:core_groupconfig_changelist"),
                    },
                    {
                        "title": "Testimonials",
                        "icon": "star",
                        "link": reverse_lazy("admin:core_testimonial_changelist"),
                    },
                ],
            },
            # ── System ──
            {
                "title": "System",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
            # ── Analytics ──
            {
                "title": "Analytics",
                "separator": True,
                "items": [
                    {
                        "title": "Visitors",
                        "icon": "visibility",
                        "link": reverse_lazy("admin:core_visitor_changelist"),
                    },
                    {
                        "title": "WhatsApp Clicks",
                        "icon": "phone_android",
                        "link": reverse_lazy("admin:core_whatsappclick_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": ["products.product"],
            "items": [
                {"title": "All Products",  "link": reverse_lazy("admin:products_product_changelist")},
                {"title": "Categories",    "link": reverse_lazy("admin:products_category_changelist")},
            ],
        },
        {
            "models": ["projects.project", "projects.projectimage"],
            "items": [
                {"title": "All Projects",  "link": reverse_lazy("admin:projects_project_changelist")},
            ],
        },
    ],
    "STYLES": [
        lambda request: static("css/admin_custom.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/theme_toggle.js"),
    ],
}