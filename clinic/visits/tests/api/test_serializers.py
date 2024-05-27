from django.test import RequestFactory, TestCase
from django.utils import timezone

from clinic.patients.factories import PatientFactory
from clinic.staff.factories import StaffFactory
from clinic.system_management.factories import ClinicFactory
from clinic.visits.api.v1.serializers import CreateVisitSerializer, UpdateVisitSerializer
from clinic.visits.choices import VisitType
from clinic.visits.factories import VisitFactory


class VisitSerializerTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.staff = StaffFactory.create(clinic=self.clinic)
        self.patient = PatientFactory.create(clinic=self.clinic)

        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

    def test_create_walk_in_visit(self):
        now = timezone.now()

        data = {
            "visit_type": VisitType.WALK_IN,
            "patient": self.patient,
            "date": (now + timezone.timedelta(days=1)).date(),
            "time": (now + timezone.timedelta(hours=1)).time(),
            # Add other required fields
        }
        serializer = CreateVisitSerializer(data=data, context={"request": self.request})
        visit = serializer.create(data)

        self.assertEqual(visit.visit_type, VisitType.WALK_IN)
        self.assertEqual(visit.date, now.date())
        self.assertEqual(visit.time.replace(microsecond=0), now.time().replace(microsecond=0))

    def test_create_scheduled_visit(self):
        future_date = timezone.now() + timezone.timedelta(days=1)

        data = {
            "visit_type": VisitType.SCHEDULED,
            "patient": self.patient,
            "date": future_date.date(),
            "time": future_date.time(),
            # Add other required fields
        }

        serializer = CreateVisitSerializer(data=data, context={"request": self.request})
        visit = serializer.create(data)

        self.assertEqual(visit.visit_type, VisitType.SCHEDULED)
        self.assertEqual(visit.date, future_date.date())
        self.assertEqual(visit.time, future_date.time())

    def test_update_visit(self):
        visit = VisitFactory.create(
            patient=self.patient,
            visit_type=VisitType.SCHEDULED,
            date=timezone.now().date(),
            time=timezone.now().time(),
        )
        new_date = timezone.now() + timezone.timedelta(days=2)
        data = {"date": new_date.date(), "time": new_date.time()}
        serializer = UpdateVisitSerializer(instance=visit, data=data, context={"request": self.request}, partial=True)
        updated_visit = serializer.update(visit, data)

        self.assertEqual(updated_visit.date, new_date.date())
        self.assertEqual(updated_visit.time, new_date.time())

    def test_update_walk_in_visit(self):
        visit = VisitFactory.create(
            patient=self.patient, visit_type=VisitType.WALK_IN, date=timezone.now().date(), time=timezone.now().time()
        )
        data = {
            "date": (timezone.now() + timezone.timedelta(days=1)).date(),
            "time": (timezone.now() + timezone.timedelta(hours=1)).time(),
        }

        serializer = UpdateVisitSerializer(instance=visit, data=data, context={"request": self.request}, partial=True)
        updated_visit = serializer.update(visit, data)

        self.assertEqual(updated_visit.date, visit.date)
        self.assertEqual(updated_visit.time, visit.time)
