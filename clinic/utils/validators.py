from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RangeValidator:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.start > self.end:
            raise ValidationError(_("invalid range"), code="invalid")
