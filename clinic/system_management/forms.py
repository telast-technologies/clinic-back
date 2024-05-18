from django import forms
from django.conf import settings
from django.contrib.auth.models import Permission

from clinic.system_management.models import ExposedPermission


class ExposedPermissionForm(forms.ModelForm):
    permission = forms.ModelChoiceField(
        queryset=Permission.objects.filter(content_type__app_label__in=settings.ALLOWED_PERMISSIONS_APPS).exclude(
            id__in=ExposedPermission.objects.values_list("permission", flat=True)
        )
    )

    class Meta:
        model = ExposedPermission
        fields = "__all__"
