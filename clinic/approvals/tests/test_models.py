from django.test import TestCase

from clinic.approvals.factories import JoinRequestFactory
from clinic.approvals.models import JoinRequest


class JoinRequestModelTest(TestCase):
    def test_create_join_request(self):
        join_request = JoinRequestFactory.create()
        self.assertIsInstance(join_request, JoinRequest)
        self.assertIsInstance(join_request.__str__(), str)
