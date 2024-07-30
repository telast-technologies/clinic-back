"""
WSGI config for clinic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings.base import ENV


if ENV == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
elif ENV == "qa":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.qa")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    
application = get_wsgi_application()
