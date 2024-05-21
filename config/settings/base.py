"""
Django settings for clinic project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import environ
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent / "clinic"


environ.Env.read_env(os.path.join("config", ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="")
FERNET_KEY = env("FERNET_KEY", default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)


ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

INTERNAL_IPS = env.list("INTERNAL_IPS", default=[])
# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "phonenumber_field",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "dj_rest_auth",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",
    "anymail",
]

CONTROLLED_LOCAL_APPS = [
    "clinic.users",
    "clinic.system_management",
    "clinic.approvals",
]
EXPOSED_LOCAL_APPS = [
    "clinic.patients",
    "clinic.staff",
    "clinic.healthcare",
    "clinic.inventory",
]

LOCAL_APPS = CONTROLLED_LOCAL_APPS + EXPOSED_LOCAL_APPS

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "clinic.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "clinic.wsgi.application"


# corsheaders
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_ALL_ORIGINS = True

# Authentication
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# JWT Token - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timezone.timedelta(minutes=540),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timezone.timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timezone.timedelta(days=7),
    "SLIDING_TOKEN_REFRESH_LIFETIME_ALLOW_REFRESH": True,
    "SLIDING_TOKEN_LIFETIME_ALLOW_REFRESH": True,
    "REFRESH_TOKEN_LIFETIME": timezone.timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}
AUTHENTICATION_FIELDS = ["username", "email"]
# dj-rest-auth - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
REST_AUTH = {
    "USE_JWT": True,
    "USER_DETAILS_SERIALIZER": "clinic.users.api.v1.serializers.UserProfileSerializer",
    "OLD_PASSWORD_FIELD_ENABLED": True,
    "JWT_AUTH_HTTPONLY": False,
}

# allowed permissions apps
ALLOWED_PERMISSIONS_APPS = [app.split(".")[-1] for app in EXPOSED_LOCAL_APPS]

# Internationalization
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = [
    ("en", _("English")),
    ("ar", _("Arabic")),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATH = BASE_DIR / "locale"
LOCALE_PATHS = [str(LOCALE_PATH)]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# Add STATIC_ROOT setting
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# rest_framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = "EG"
# password reset
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = env.str("PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL", "http://localhost:3000")

# drf-spectacular
# https://github.com/tfranzel/drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Clinic API",
    "DESCRIPTION": """
    Clinic management involves coordinating administrative, financial, and clinical tasks.
    clinic management is a comprehensive healthcare management system that provides a centralized platform as following
    1- encompasses appointment scheduling.
    2- patient registration.
    3- electronic health records management.
    4- billing.
    5- inventory control.
    6- staff optimization.
    7- regulatory compliance.
    8- Effective management enhances patient experiences.
    9- streamlines workflows.
    10- improves overall clinic performance.
    """,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
}
CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")
# Option: CDN
CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "cdn.jsdelivr.net")

# drf-nested-multipart-parser
# https://github.com/tfranzel/drf-nested-multipart-parser
DRF_NESTED_MULTIPART_PARSER = {
    "separator": "bracket",
    "raise_duplicate": True,
    "assign_duplicate": False,
    # # output of parser is converted to querydict
    # # if is set to False, dict python is returned
    "querydict": False,
}

# Email
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"  # or sendgrid.EmailBackend, or...
ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": env.str("MAILGUN_API_KEY", default=""),
    "MAILGUN_SENDER_DOMAIN": env.str("MAILGUN_SENDER_DOMAIN", default=""),  # your Mailgun domain, if needed
}
# email from which all outgoing emails will be sent (for security reasons)
# if you don't already have this in settings
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="")  # default from-email for Django errors
SERVER_EMAIL = env.str("MAILGUN_SERVER_EMAIL", default="")  # ditto (default from-email for Django errors)

# Debug Toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}
