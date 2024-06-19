from datetime import date, time, timedelta

from django.test import TestCase

from clinic.patients.factories import PatientFactory
from clinic.system_management.factories import ClinicFactory
from clinic.system_management.services.clinic_service import ClinicService
from clinic.visits.choices import VisitStatus, VisitType
from clinic.visits.factories import TimeSlotFactory, VisitFactory


class ClinicServiceTests(TestCase):
    def setUp(self):
        # Create a clinic
        self.clinic = ClinicFactory.create(name="Test Clinic", capacity=10)
        TimeSlotFactory.create(
            clinic=self.clinic,
            days=["monday", "tuesday", "wednesday", "thursday"],
            start_time="10:00:00",
            end_time="11:00:00",
        )
        TimeSlotFactory.create(
            clinic=self.clinic,
            days=["monday", "tuesday", "wednesday", "thursday"],
            start_time="14:00:00",
            end_time="16:00:00",
        )
        # Initialize the ClinicService
        self.service = ClinicService(clinic=self.clinic)

    def test_get_available_dates(self):
        # Create visits for the patient within the next 31 days
        today = date.today()
        visit_dates = [today + timedelta(days=i) for i in range(5, 10)]
        # Create a patient
        patient = PatientFactory.create(clinic=self.clinic)
        for visit_date in visit_dates:
            # Create a visit
            VisitFactory.create(
                patient=patient,
                date=visit_date,
                time=time(hour=10),
                visit_type=VisitType.SCHEDULED,
                status=VisitStatus.BOOKED,
            )

        available_dates = self.service.get_available_dates(patient_id=patient.pk)
        expected_dates = [
            today + timedelta(days=i)
            for i in range(31)
            if (today + timedelta(days=i)) not in visit_dates
            and (today + timedelta(days=i)).strftime("%A").lower() in self.clinic.days
        ]

        self.assertEqual(available_dates, expected_dates)

    def test_get_available_slots(self):
        # Set the date for testing
        monday = date(2024, 5, 27)

        test_date = monday + timedelta(days=(7 - monday.weekday()))  # Next Monday

        # Create visits for the given date
        for hour in [9, 10, 11]:  # Book the morning slots
            for _ in range(self.clinic.capacity):
                # Create a patient
                patient = PatientFactory.create(clinic=self.clinic)
                # Create a visit
                VisitFactory.create(
                    patient=patient,
                    date=test_date,
                    time=time(hour=hour),
                    visit_type=VisitType.SCHEDULED,
                    status=VisitStatus.BOOKED,
                )

        available_slots = self.service.get_available_slots(test_date)
        expected_slots = [time(hour=14), time(hour=15), time(hour=16)]  # The available afternoon slots

        self.assertEqual(available_slots, expected_slots)

    def test_get_available_slots_day_off(self):
        # Set the date for testing
        test_date = date(2024, 5, 31)  # Friday

        available_slots = self.service.get_available_slots(test_date)
        expected_slots = []  # The available afternoon slots

        self.assertEqual(available_slots, expected_slots)
