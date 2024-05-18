from django.test import TestCase

from clinic.users.factories import UserFactory
from clinic.users.models import User


class UserTestCase(TestCase):
    def test_create_user(self):
        user = UserFactory.create()
        assert isinstance(user, User)
        assert isinstance(user.__str__(), str)
