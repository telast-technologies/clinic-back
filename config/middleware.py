import logging
import re
from collections.abc import Callable
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

from clinic.system_management.models import Clinic

# Initializing logger for logging errors and information
logger = logging.getLogger(__name__)


class ClinicWhiteListMiddleware:
    # Generating error message when access is restricted
    error_msg: str = _("Unable to determine your clinic or access is restricted.")

    def __init__(self, get_response: Callable[[Any, Any], Any]) -> None:
        self.get_response: Callable[[Any, Any], Any] = get_response

    def __call__(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponseForbidden | None:
        # Checking if the request is valid based on the defined logic
        if not self.isvalid(request):
            # Logging the error message
            logger.error(ClinicWhiteListMiddleware.error_msg)
            # Returning a forbidden response with the error message
            return HttpResponseForbidden(ClinicWhiteListMiddleware.error_msg)

        # If the request is valid, proceed with the normal response
        response: HttpResponseForbidden | None = self.get_response(request, *args, **kwargs)
        return response

    def isvalid(self, request: Any) -> bool:
        # Checking if the request is for an API endpoint
        is_api: bool = bool(re.search(r"^/api/", request.path_info))
        # Checking if the server is in test mode
        test_mode: bool = request.META.get("SERVER_NAME", "") == "testserver"
        # Checking if the server is in debug mode
        debug_mode: bool = settings.DEBUG

        # If development mode or the admin
        if test_mode or debug_mode or not is_api:
            return True
        if is_api and not hasattr(request.user, "staff"):
            return False

        # If not, proceed with country whitelist validation
        cache_key: str = "clinic-whitelist"
        cached_data: bool | None = cache.get(cache_key)

        # If cached data is available, use it directly
        if cached_data is not None:
            return cached_data
        else:
            clinic: Clinic | None = getattr(request.user.staff, "clinic", None)
            allowed: bool = clinic and getattr(request.user.staff.clinic, "active", False)
            # Caching the result for 10 seconds
            cache.set(cache_key, allowed, 10)
            return allowed
