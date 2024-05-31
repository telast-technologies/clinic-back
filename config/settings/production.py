from config.settings.base import *  # noqa
from config.settings.base import INSTALLED_APPS, MIDDLEWARE, env

# https://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
INSTALLED_APPS += ["whitenoise.runserver_nostatic"]
# SECURITY WARNING: don't run with debug turned on in production!
MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
# SECURITY
# ------------------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = ["https://*.clinic.telast.tech"]
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
CORS_ALLOWED_ORIGINS = ["https://*.clinic.telast.tech"]
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa: F405
# STATIC
# ------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "media": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
