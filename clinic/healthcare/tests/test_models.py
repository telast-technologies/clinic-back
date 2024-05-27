from django.test import TestCase

from clinic.healthcare.factories import ServiceFactory
from clinic.healthcare.models import Service


class ServiceModelTest(TestCase):
    def test_create_service(self):
        service = ServiceFactory.create()
        self.assertIsInstance(service, Service)
        self.assertIsInstance(service.__str__(), str)
