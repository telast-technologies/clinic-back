from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from clinic.approvals.admin import JoinRequestAdmin
from clinic.approvals.choices import JoinRequestStatusChoices
from clinic.approvals.factories import JoinRequestFactory
from clinic.approvals.models import JoinRequest
from clinic.staff.models import Staff
from clinic.system_management.factories import ClinicFactory
from clinic.system_management.models import Clinic
from clinic.users.factories import UserFactory
from clinic.users.models import User


class JoinRequestAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = JoinRequestAdmin(JoinRequest, self.site)
        self.request = RequestFactory().get("/fake-url/")
        self.join_request = JoinRequestFactory.create()

    def test_approve_join_request(self):
        self.join_request.status = JoinRequestStatusChoices.APPROVED
        self.admin.save_model(self.request, self.join_request, None, None)

        # Check that the clinic, user, and staff were created
        self.assertTrue(Clinic.objects.filter(name=self.join_request.clinic_name).exists())
        self.assertTrue(User.objects.filter(email=self.join_request.administrator_email).exists())
        self.assertTrue(Staff.objects.filter(user__email=self.join_request.administrator_email).exists())

    def test_reject_join_request(self):
        self.join_request.status = JoinRequestStatusChoices.REJECTED
        self.admin.save_model(self.request, self.join_request, None, None)

        self.assertFalse(Clinic.objects.filter(name=self.join_request.clinic_name).exists())
        self.assertFalse(User.objects.filter(email=self.join_request.administrator_email).exists())
        self.assertFalse(Staff.objects.filter(user__email=self.join_request.administrator_email).exists())

    def test_approve_join_request_with_existing_user_email(self):
        # Create a user with the same email
        user = UserFactory.create()
        join_request = JoinRequestFactory.create(administrator_email=user.email)
        join_request.status = JoinRequestStatusChoices.APPROVED

        with self.assertRaises(ValueError) as context:
            self.admin.save_model(self.request, join_request, None, None)

        self.assertEqual(str(context.exception), "data already exists")

    def test_approve_join_request_with_existing_user_phone(self):
        # Create a user with the same phone number
        user = UserFactory.create()
        join_request = JoinRequestFactory.create(administrator_phone=user.phone)
        join_request.status = JoinRequestStatusChoices.APPROVED

        with self.assertRaises(ValueError) as context:
            self.admin.save_model(self.request, join_request, None, None)

        self.assertEqual(str(context.exception), "data already exists")

    def test_approve_join_request_with_existing_clinic_name(self):
        # Create a clinic with the same name
        clinic = ClinicFactory.create()
        join_request = JoinRequestFactory.create(clinic_name=clinic.name)
        join_request.status = JoinRequestStatusChoices.APPROVED

        with self.assertRaises(ValueError) as context:
            self.admin.save_model(self.request, join_request, None, None)

        self.assertEqual(str(context.exception), "data already exists")
