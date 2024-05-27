from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PasswordValidator:
    requires_context = True

    def __call__(self, attr: str, serializer: serializers.ModelSerializer):
        request_method = serializer.context["request"].method

        password = attr.get("password", None)
        password_confirm = attr.get("password_confirm", None)

        if any(
            [
                request_method == "POST" and not (password and password_confirm),
                request_method in ["PATCH", "PUT"] and (password and not password_confirm),
                request_method in ["PATCH", "PUT"] and (not password and password_confirm),
                (password and password_confirm) and password != password_confirm,
            ]
        ):
            raise serializers.ValidationError({"password": _("invalid or missing password")})
