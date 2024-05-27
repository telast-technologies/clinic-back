from django.conf import settings
from django.contrib.auth.models import Permission
from django.test import TestCase

from clinic.staff.factories import StaffFactory
from clinic.users.choices import Roles
from clinic.users.factories import UserFactory
from clinic.users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_create_user(self):
        assert isinstance(self.user, User)
        assert isinstance(self.user.__str__(), str)

    def test_display_role_not_staff(self):
        self.assertEqual(self.user.role, Roles.OTHER)

    def test_display_permissions_not_staff(self):
        self.assertEqual(list(self.user.permissions), list(Permission.objects.none()))

    def test_display_clinic_not_staff(self):
        self.assertEqual(self.user.clinic, None)

    def test_display_role_staff(self):
        StaffFactory.create(user=self.user)
        self.assertEqual(self.user.role, Roles.STAFF)

    def test_display_permissions_staff(self):
        staff = StaffFactory.create(user=self.user)
        permissions = Permission.objects.filter(id__in=staff.permissions.values_list("permission", flat=True))
        self.assertEqual(list(self.user.permissions), list(permissions))

    def test_display_permissions_client_admin_staff(self):
        StaffFactory.create(user=self.user, is_client_admin=True)
        permissions = Permission.objects.filter(content_type__app_label__in=settings.ALLOWED_PERMISSIONS_APPS)
        self.assertEqual(list(self.user.permissions), list(permissions))

    def test_display_clinic_staff(self):
        staff = StaffFactory.create(user=self.user)
        self.assertEqual(self.user.clinic, staff.clinic)
