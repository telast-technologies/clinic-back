"""
ASGI config for clinic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from config.settings.base import ENV

if ENV == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
elif ENV == "qa":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.qa")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = get_asgi_application()
