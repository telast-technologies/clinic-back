from typing import Any

from django.contrib import admin
from django.db import transaction
from django.http import HttpRequest
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from clinic.approvals.choices import JoinRequestStatusChoices
from clinic.approvals.models import JoinRequest
from clinic.staff.models import Staff
from clinic.system_management.models import Clinic
from clinic.users.models import User
from clinic.utils.notifications import send_email


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "administrator_first_name",
        "administrator_last_name",
        "clinic_name",
        "package",
        "created_at",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("administrator_first_name", "administrator_last_name", "clinic_name")
    readonly_fields = (
        "uid",
        "administrator_first_name",
        "administrator_last_name",
        "administrator_email",
        "administrator_phone",
        "clinic_name",
        "clinic_description",
        "clinic_address",
        "clinic_phone",
        "clinic_email",
        "clinic_website",
        "package",
        "created_at",
        "updated_at",
    )

    @transaction.atomic
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> Any:
        if (not obj.tracker.previous("status") == JoinRequestStatusChoices.APPROVED) and (
            obj.status == JoinRequestStatusChoices.APPROVED
        ):
            # create clinic data
            clinic_data = {
                "name": obj.clinic_name,
                "description": obj.clinic_description,
                "address": obj.clinic_address,
                "phone": obj.clinic_phone,
                "email": obj.clinic_email,
                "website": obj.clinic_website,
                "package": obj.package,
            }
            # create username and password
            username = get_random_string(length=10)
            password = get_random_string(length=10)
            # create staff
            user_data = {
                "first_name": obj.administrator_first_name,
                "last_name": obj.administrator_last_name,
                "email": obj.administrator_email,
                "phone": obj.administrator_phone,
                "username": username,
                "password": password,
            }

            clinic = Clinic.objects.create(**clinic_data)
            user = User.objects.create(**user_data)
            # create staff
            staff_data = {"user": user, "clinic": clinic}
            staff = Staff.objects.create(**staff_data, is_client_admin=True)

            subject = _("Join Request Approved")
            message = f"""
                Hello {staff.user.get_full_name()},
                Congratulations! Your Join Request has been approved.
                Here are your credentials as following:
                email: {staff.user.email}
                Password: {password}",
                Best regards,
                Clinic Team
            """
            send_email(recipient_list=[staff.user.email], subject=subject, message=message)

        elif (not obj.tracker.previous("status") == JoinRequestStatusChoices.REJECTED) and (
            obj.status == JoinRequestStatusChoices.REJECTED
        ):
            subject = _("Join Request Rejected")
            message = f"""
                Hello {obj.administrator_first_name} {obj.administrator_last_name},
                Your Join Request has been rejected. you can contact the administrator for more details.
                Best regards,
                Clinic Team
            """
            send_email(recipient_list=[obj.administrator_email], subject=subject, message=message)

        return super().save_form(request, form, change)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False