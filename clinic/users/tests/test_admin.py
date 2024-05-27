from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from clinic.users.admin import UserAdmin
from clinic.users.factories import UserFactory
from clinic.users.models import User


class UserAdminTest(TestCase):
    def setUp(self):
        self.admin = UserAdmin(User, AdminSite())
        self.obj = UserFactory.create()
        self.request = RequestFactory().get("/fake-url/")
        self.request.user = self.obj

        self.client.force_login(self.obj)

    def test_display_role(self):
        self.assertEqual(self.obj.role, self.admin.display_role(self.obj))

    def test_get_queryset(self):
        self.assertNotIn(self.obj, list(self.admin.get_queryset(self.request)))
