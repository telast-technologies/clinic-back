from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PackageActiveStatusValidator:
    def __call__(self, value):
        if not value.active:
            raise ValidationError(_("Package is not active"))

    def __eq__(self, other):
        return isinstance(other, self.__class__)
