from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ChargeItemValidator:
    requires_context = True
    message = _("Invalid invoice data")

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        if any(
            [
                attrs["invoice"].visit.patient.clinic != serializer.context["request"].user.staff.clinic,
                attrs["supply"].clinic != serializer.context["request"].user.staff.clinic,
                attrs["quantity"] > attrs["supply"].remains,
            ]
        ):
            raise serializers.ValidationError({"invoice": self.message})


class ChargeServiceValidator:
    requires_context = True
    message = _("Invalid invoice data")

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        if any(
            [
                attrs["invoice"].visit.patient.clinic != serializer.context["request"].user.staff.clinic,
                attrs["service"].clinic != serializer.context["request"].user.staff.clinic,
                not attrs["service"].active,
            ]
        ):
            raise serializers.ValidationError({"invoice": self.message})
