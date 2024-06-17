from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from clinic.system_management.admin_actions import ClinicActivationAdminAction, PackageActivationAdminAction
from clinic.system_management.factories import ClinicFactory, PackageFactory
from clinic.system_management.models import Clinic, Package


class ClinicActivationAdminActionTest(TestCase):
    def setUp(self):
        # initialize the request
        self.rf = RequestFactory().get("/")
        self.sm = SessionMiddleware(get_response=lambda request: HttpResponse())
        self.mm = MessageMiddleware(get_response=lambda request: HttpResponse())
        # addidtional middleware
        self.prepare_request()

        self.action_instance = ClinicActivationAdminAction()

        return super().setUp()

    def prepare_request(self):
        self.sm.process_request(self.rf)
        self.mm.process_request(self.rf)

    def test_active_user_action(self):
        clinic = ClinicFactory.create(active=False)
        queryset = Clinic.objects.filter(pk=clinic.pk)

        self.action_instance.activate(self.rf, queryset)

        clinic.refresh_from_db()

        self.assertTrue(clinic.active)

        # Check if success message is present in the messages
        messages = get_messages(self.rf)
        self.assertEqual(len(messages), 1)
        # Check if success message is correct
        message = list(messages)[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, "the status change to Active")

    def test_deactive_user_action(self):
        clinic = ClinicFactory.create(active=True)
        queryset = Clinic.objects.filter(pk=clinic.pk)

        self.action_instance.deactivate(self.rf, queryset)

        clinic.refresh_from_db()

        self.assertFalse(clinic.active)

        # Check if success message is present in the messages
        messages = get_messages(self.rf)
        self.assertEqual(len(messages), 1)
        # Check if success message is correct
        message = list(messages)[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, "the status change to Inactive")


class PackageActivationAdminActionTest(TestCase):
    def setUp(self):
        # initialize the request
        self.rf = RequestFactory().get("/")
        self.sm = SessionMiddleware(get_response=lambda request: HttpResponse())
        self.mm = MessageMiddleware(get_response=lambda request: HttpResponse())
        # addidtional middleware
        self.prepare_request()

        self.action_instance = PackageActivationAdminAction()

        return super().setUp()

    def prepare_request(self):
        self.sm.process_request(self.rf)
        self.mm.process_request(self.rf)

    def test_active_user_action(self):
        package = PackageFactory.create(active=False)
        queryset = Package.objects.filter(pk=package.pk)

        self.action_instance.activate(self.rf, queryset)

        package.refresh_from_db()

        self.assertTrue(package.active)

        # Check if success message is present in the messages
        messages = get_messages(self.rf)
        self.assertEqual(len(messages), 1)
        # Check if success message is correct
        message = list(messages)[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, "the status change to Active")

    def test_deactive_user_action(self):
        package = PackageFactory.create(active=True)
        queryset = Package.objects.filter(pk=package.pk)

        self.action_instance.deactivate(self.rf, queryset)

        package.refresh_from_db()

        self.assertFalse(package.active)

        # Check if success message is present in the messages
        messages = get_messages(self.rf)
        self.assertEqual(len(messages), 1)
        # Check if success message is correct
        message = list(messages)[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, "the status change to Inactive")
