from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from clinic.invoices.factories import ChargeItemFactory, InvoiceFactory
from clinic.patients.factories import PatientFactory
from clinic.staff.factories import StaffFactory
from clinic.visits.choices import VisitStatus, VisitType
from clinic.visits.factories import TimeSlotFactory, VisitFactory


class VisitViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = StaffFactory.create(is_client_admin=True)
        self.visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic),
        )
        self.client.force_authenticate(user=self.staff.user)

    def test_retrieve_visit_list(self):
        # Test retrieving visit list
        VisitFactory.create()

        url = reverse("api:v1:visits:visit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_invalid_retrieve_visit_detail(self):
        visit = VisitFactory.create()
        # Test retrieving visit detail
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": visit.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_retrieve_visit_detail(self):
        # Test retrieving visit detail
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic),
        )
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": visit.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_visit_invalid_missing_data(self):
        # Test creating visit with invalid data
        url = reverse("api:v1:visits:visit-list")
        invalid_data = {}
        response = self.client.post(url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_visit_missing_instance(self):
        # Test updating non-existing visit instance
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": 9999})  # Non-existing visit pk
        data = {}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_visit_missing_instance(self):
        # Test deleting non-existing visit instance
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": 9999})  # Non-existing visit pk
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_delete_visit_invalid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create()
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": visit.pk})
        data = {}
        response = self.client.delete(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_update_visit_invalid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create()
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": visit.pk})
        data = {}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_visit_valid_data(self):
        # Test updating visit with valid data
        TimeSlotFactory.create(days=["monday"], clinic=self.staff.clinic, start_time="10:00:00", end_time="13:00:00")
        monday = date(2024, 5, 27)

        url = reverse("api:v1:visits:visit-list")
        data = {
            "patient": PatientFactory.create(clinic=self.staff.clinic).pk,
            "date": monday,
            "time": "10:00:00",
            "status": VisitStatus.BOOKED,
            "visit_type": VisitType.SCHEDULED,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_visit_valid_data(self):
        # Test updating visit with valid data
        TimeSlotFactory.create(days=["monday"], clinic=self.staff.clinic, start_time="10:00:00", end_time="13:00:00")
        monday = date(2024, 5, 27)

        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic),
        )
        url = reverse("api:v1:visits:visit-detail", kwargs={"pk": visit.pk})
        data = {"date": monday, "time": "10:00:00"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_arrived_visit_valid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.BOOKED)
        url = reverse("api:v1:visits:visit-arrive", kwargs={"pk": visit.pk})
        response = self.client.patch(url, data={"purpose": "examination"}, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(visit.status, VisitStatus.ARRIVED)
        self.assertIsNotNone(visit.arrival_info)
        self.assertTrue(hasattr(visit, "invoice"))

    def test_arrived_visit_invalid_purpose_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.BOOKED)
        url = reverse("api:v1:visits:visit-arrive", kwargs={"pk": visit.pk})
        response = self.client.patch(url, data={"purpose": "OTHER"}, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_arrived_visit_invalid_status_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.CHECKED_IN
        )
        url = reverse("api:v1:visits:visit-arrive", kwargs={"pk": visit.pk})
        response = self.client.patch(url, data={"purpose": "examination"}, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(visit.status, VisitStatus.CHECKED_IN)

    def test_check_in_visit_valid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.ARRIVED
        )
        url = reverse("api:v1:visits:visit-check-in", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(visit.status, VisitStatus.CHECKED_IN)

    def test_check_in_invalid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.CHECKED_OUT
        )
        url = reverse("api:v1:visits:visit-check-in", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(visit.status, VisitStatus.CHECKED_OUT)
        self.assertFalse(hasattr(visit, "invoice"))

    def test_check_out_valid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.CHECKED_IN
        )
        invoice = InvoiceFactory.create(visit=visit)
        charge_item = ChargeItemFactory.create(invoice=invoice)
        charge_item.supply.quantity = 5
        charge_item.supply.save()

        url = reverse("api:v1:visits:visit-check-out", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(visit.status, VisitStatus.CHECKED_OUT)

    def test_check_out_invalid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.BOOKED)
        url = reverse("api:v1:visits:visit-check-out", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(visit.status, VisitStatus.BOOKED)

    def test_cancel_book_visit_valid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.BOOKED)
        url = reverse("api:v1:visits:visit-cancel", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(visit.status, VisitStatus.CANCELLED)
        self.assertEqual(visit.comment, "")

    def test_cancel_checked_in_visit_valid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.CHECKED_IN
        )
        url = reverse("api:v1:visits:visit-cancel", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(visit.status, VisitStatus.CANCELLED)
        self.assertEqual(visit.comment, "")

    def test_cancel_checked_in_visit_valid_data_with_reason(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.CHECKED_IN
        )
        url = reverse("api:v1:visits:visit-cancel", kwargs={"pk": visit.pk})
        response = self.client.patch(url, data={"reason": "test"}, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(visit.status, VisitStatus.CANCELLED)
        self.assertEqual(visit.comment, "test")

    def test_cancel_check_out_visit_invalid_data(self):
        # Test updating visit with valid data
        visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic), status=VisitStatus.CHECKED_OUT
        )
        url = reverse("api:v1:visits:visit-cancel", kwargs={"pk": visit.pk})
        response = self.client.patch(url, format="json")

        visit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(visit.status, VisitStatus.CHECKED_OUT)


class VisitAvailableDatesViewTest(TestCase):
    def setUp(self):
        self.staff = StaffFactory.create(is_client_admin=True)

        self.client = APIClient()
        self.client.force_authenticate(user=self.staff.user)

    def test_valid_retrieve_visit_available_dates(self):
        # Test retrieving visit available dates
        patient = PatientFactory.create(clinic=self.staff.clinic)
        url = reverse("api:v1:visits:slots_date_available", kwargs={"patient": f"{patient.pk}"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VisitAvailableSlotsViewTest(TestCase):
    def setUp(self):
        self.staff = StaffFactory.create(is_client_admin=True)

        self.client = APIClient()
        self.client.force_authenticate(user=self.staff.user)

    def test_valid_retrieve_visit_available_slots(self):
        # Test retrieving visit available slots
        url = reverse("api:v1:visits:slots_time_available", kwargs={"date": date(2024, 5, 27)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VisitQueueViewTest(TestCase):
    def setUp(self):
        self.staff = StaffFactory.create(is_client_admin=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.staff.user)
        self.url = reverse("api:v1:visits:today_queue")

    def test_valid_retrieve_today_queue(self):
        patient1 = PatientFactory(first_name="John", last_name="Doe", clinic=self.staff.clinic)
        patient2 = PatientFactory(first_name="Jane", last_name="Doe", clinic=self.staff.clinic)
        patient3 = PatientFactory(first_name="Alice", last_name="Smith", clinic=self.staff.clinic)

        VisitFactory(
            patient=patient1,
            date=date.today(),
            status=VisitStatus.ARRIVED,
            arrival_info={"purpose": "examination", "date": str(date.today()), "queue": 1},
        )
        VisitFactory(
            patient=patient2,
            date=date.today(),
            status=VisitStatus.ARRIVED,
            arrival_info={"purpose": "examination", "date": str(date.today()), "queue": 2},
        )
        VisitFactory(
            patient=patient3,
            date=date.today(),
            status=VisitStatus.ARRIVED,
            arrival_info={"purpose": "consultant", "date": str(date.today()), "queue": 1},
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("examination", response.data)
        self.assertIn("consultant", response.data)
        self.assertEqual(response.data["examination"][0]["patient"], "John Doe")
        self.assertEqual(response.data["consultant"][0]["queue"], 1)

    def test_no_visits_returns_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_excludes_non_arrived_visits(self):
        VisitFactory(
            date=date.today(),
            status=VisitStatus.BOOKED,
            arrival_info={"purpose": "examination", "date": str(date.today()), "queue": 1},
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_missing_arrival_info(self):
        VisitFactory(date=date.today(), status=VisitStatus.ARRIVED, arrival_info={})  # Missing purpose and queue
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_permission_denied_for_non_admin(self):
        staff = StaffFactory.create(is_client_admin=False)
        self.client.force_authenticate(user=staff.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReorderQueueAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = StaffFactory.create(is_client_admin=True)
        self.client.force_authenticate(user=self.staff.user)

        self.patient1 = PatientFactory(first_name="John", last_name="Doe", clinic=self.staff.clinic)
        self.patient2 = PatientFactory(first_name="Jane", last_name="Doe", clinic=self.staff.clinic)

        self.visit1 = VisitFactory.create(
            patient=self.patient1,
            date=date.today(),
            status=VisitStatus.ARRIVED,
            arrival_info={"purpose": "examination", "date": str(date.today()), "queue": 1},
        )
        self.visit2 = VisitFactory.create(
            patient=self.patient2,
            date=date.today(),
            status=VisitStatus.ARRIVED,
            arrival_info={"purpose": "examination", "date": str(date.today()), "queue": 2},
        )

        self.url = reverse("api:v1:visits:reorder_queue")

    def test_reorder_queue_successfully(self):
        data = [
            {"visit_pk": str(self.visit2.pk), "queue": 1},
            {"visit_pk": str(self.visit1.pk), "queue": 2},
        ]

        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("examination", response.data)
        self.assertEqual(response.data["examination"][0]["visit_pk"], str(self.visit2.pk))
        self.assertEqual(response.data["examination"][1]["visit_pk"], str(self.visit1.pk))

    def test_reorder_queue_invalid_user(self):
        # Auth as non-admin staff
        non_admin = StaffFactory.create(is_client_admin=False)
        self.client.force_authenticate(user=non_admin.user)

        data = [{"visit_pk": str(self.visit1.pk), "queue": 1}]
        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class VisitCalendarViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = StaffFactory.create(is_client_admin=True)
        self.visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic),
        )
        self.client.force_authenticate(user=self.staff.user)

    def test_retrieve_visit_list(self):
        # Test retrieving visit list
        VisitFactory.create()

        url = reverse("api:v1:visits:visit-calendar")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
