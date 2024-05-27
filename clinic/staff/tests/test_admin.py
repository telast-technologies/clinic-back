from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from clinic.staff.admin import StaffAdmin
from clinic.staff.factories import StaffFactory
from clinic.staff.models import Staff


class StaffAdminTest(TestCase):
    def setUp(self):
        self.admin = StaffAdmin(Staff, AdminSite())
        self.obj = StaffFactory.create()
        self.request = RequestFactory().get("/fake-url/")
        self.request.user = self.obj.user

        self.client.force_login(self.obj.user)

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))

    def test_get_queryset(self):
        self.assertNotIn(self.obj, list(self.admin.get_queryset(self.request)))
