from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.visits.admin import VisitAdmin
from clinic.visits.factories import VisitFactory
from clinic.visits.models import Visit


class VisitAdminTest(TestCase):
    def setUp(self):
        self.admin = VisitAdmin(Visit, AdminSite())
        self.obj = VisitFactory.create()
        self.request = None

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))
