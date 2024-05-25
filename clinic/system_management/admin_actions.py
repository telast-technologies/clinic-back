from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from clinic.system_management.models import Clinic


class ActivationAdminAction:
    @transaction.atomic
    def activate(self, request, queryset):
        Clinic.objects.filter(pk__in=queryset.values_list("uid", flat=True)).update(active=True)
        messages.success(request, _("the status change to Active"))

    @transaction.atomic
    def deactivate(self, request, queryset):
        Clinic.objects.filter(pk__in=queryset.values_list("uid", flat=True)).update(active=False)
        messages.success(request, _("the status change to Deactive"))
