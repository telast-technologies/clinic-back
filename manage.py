#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from config.settings.base import ENV


def main():
    """Run administrative tasks."""
    if ENV == "local":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    elif ENV == "qa":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.qa")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
