from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from rest_framework import viewsets

from clinic.staff.factories import StaffFactory
from clinic.system_management.factories import ClinicFactory
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.factories import UserFactory
from clinic.visits.factories import TimeSlotFactory
from clinic.visits.models import TimeSlot


class QuerysetFilteredMixinTest(TestCase):
    class MockAPIView(QuerysetFilteredMixin, viewsets.GenericViewSet):
        queryset = TimeSlot.objects.all()
        serializer_class = None

    def setUp(self):
        self.factory = RequestFactory()

        # Create test data
        self.clinic1 = ClinicFactory.create(name="Clinic 1")
        self.clinic2 = ClinicFactory.create(name="Clinic 2")

        self.user1 = UserFactory.create(username="user1", password="password1")
        self.user2 = UserFactory.create(username="user2", password="password2")

        self.staff1 = StaffFactory.create(user=self.user1, clinic=self.clinic1)
        self.staff2 = StaffFactory.create(user=self.user2, clinic=self.clinic2)

        self.model1 = TimeSlotFactory.create(clinic=self.clinic1)
        self.model2 = TimeSlotFactory.create(clinic=self.clinic2)

        self.view = QuerysetFilteredMixinTest.MockAPIView()

    def test_get_queryset_with_staff_user(self):
        request = self.factory.get("/")
        request.user = self.user1

        self.view.request = request

        queryset = self.view.get_queryset()
        self.assertEqual(list(queryset), [self.model1])

    def test_get_queryset_with_non_staff_user(self):
        non_staff_user = UserFactory.create(username="nonstaff", password="password")
        request = self.factory.get("/")
        request.user = non_staff_user

        self.view.request = request

        queryset = self.view.get_queryset()
        self.assertEqual(list(queryset), [])

    def test_get_queryset_with_no_user(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()

        self.view.request = request

        queryset = self.view.get_queryset()
        self.assertEqual(list(queryset), [])
