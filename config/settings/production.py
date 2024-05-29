from config.settings.base import *  # noqa
from config.settings.base import MIDDLEWARE, env

# SECURITY WARNING: don't run with debug turned on in production!
MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa: F405

# STATIC
# ------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
