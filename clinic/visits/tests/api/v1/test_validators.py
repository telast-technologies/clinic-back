from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.utils import timezone
from rest_framework import serializers

from clinic.healthcare.factories import ServiceFactory
from clinic.inventory.factories import SupplyFactory
from clinic.patients.factories import PatientFactory
from clinic.staff.factories import StaffFactory
from clinic.system_management.factories import ClinicFactory
from clinic.visits.api.v1.serializers import (
    ChargeServiceModifySerializer,
    CreateChargeItemSerializer,
    CreateVisitSerializer,
)
from clinic.visits.api.v1.validators import ChargeItemValidator, ChargeServiceValidator, VisitValidator
from clinic.visits.choices import VisitStatus, VisitType
from clinic.visits.factories import VisitFactory


class VisitValidatorTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.other_clinic = ClinicFactory.create(name="Other Clinic")

        self.staff = StaffFactory.create(clinic=self.clinic)

        self.patient = PatientFactory.create(clinic=self.clinic)
        self.other_patient = PatientFactory.create(clinic=self.other_clinic)

        self.visit = VisitFactory.create(
            patient=self.patient,
            date=timezone.now().date(),
            time=timezone.now().time(),
            status=VisitStatus.BOOKED,
            visit_type=VisitType.SCHEDULED,
        )
        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        self.validator = VisitValidator()

    @patch("clinic.visits.api.v1.validators.ClinicService.get_available_slots")
    def test_patient_clinic_mismatch(self, mock_get_available_slots):
        serializer = CreateVisitSerializer(instance=self.visit, context={"request": self.request})
        attrs = {"patient": self.other_patient}
        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("patient", context.exception.detail)
        self.assertIn("Patient does not belong to the same clinic.", context.exception.detail["patient"])

    @patch("clinic.visits.api.v1.validators.ClinicService.get_available_slots")
    def test_time_slot_unavailable(self, mock_get_available_slots):
        mock_get_available_slots.return_value = []  # Mock no available slots
        serializer = CreateVisitSerializer(instance=self.visit, context={"request": self.request})
        attrs = {"date": self.visit.date, "time": self.visit.time}
        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("time", context.exception.detail)
        self.assertIn("Selected time slot is not available.", context.exception.detail["time"])

    @patch("clinic.visits.api.v1.validators.ClinicService.get_available_slots")
    def test_valid_data(self, mock_get_available_slots):
        # Mock available slots to include the visit time
        mock_get_available_slots.return_value = [self.visit.time]
        serializer = CreateVisitSerializer(instance=self.visit, context={"request": self.request})
        attrs = {
            "patient": self.patient,
            "date": self.visit.date,
            "time": self.visit.time,
            "visit_type": VisitType.SCHEDULED,
        }
        try:
            self.validator(attrs, serializer)
        except serializers.ValidationError:
            self.fail("VisitValidator raised ValidationError unexpectedly!")


class ChargeItemValidatorTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.other_clinic = ClinicFactory.create(name="Other Clinic")

        self.staff = StaffFactory.create(clinic=self.clinic)
        self.patient = PatientFactory.create(clinic=self.clinic)
        self.other_patient = PatientFactory.create(clinic=self.other_clinic)

        self.visit = VisitFactory.create(patient=self.patient)
        self.other_visit = VisitFactory.create(patient=self.other_patient)

        self.supply = SupplyFactory.create(clinic=self.clinic, quantity=10)
        self.other_supply = SupplyFactory.create(clinic=self.other_clinic, quantity=10)

        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        self.validator = ChargeItemValidator()

    def test_invalid_visit_clinic(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"visit": self.other_visit, "supply": self.supply, "quantity": 1}
        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("visit", context.exception.detail)
        self.assertIn("Invalid visit data", context.exception.detail["visit"])

    def test_invalid_supply_clinic(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"visit": self.visit, "supply": self.other_supply, "quantity": 1}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("visit", context.exception.detail)
        self.assertIn("Invalid visit data", context.exception.detail["visit"])

    def test_insufficient_supply(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"visit": self.visit, "supply": self.supply, "quantity": 11}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("visit", context.exception.detail)
        self.assertIn("Invalid visit data", context.exception.detail["visit"])

    def test_valid_charge_item(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"visit": self.visit, "supply": self.supply, "quantity": 5}

        try:
            self.validator(attrs, serializer)
        except serializers.ValidationError:
            self.fail("ChargeItemValidator raised ValidationError unexpectedly!")


class ChargeServiceValidatorTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.other_clinic = ClinicFactory.create(name="Other Clinic")

        self.staff = StaffFactory.create(clinic=self.clinic)
        self.patient = PatientFactory.create(clinic=self.clinic)
        self.other_patient = PatientFactory.create(clinic=self.other_clinic)

        self.visit = VisitFactory.create(patient=self.patient)
        self.other_visit = VisitFactory.create(patient=self.other_patient)

        self.service = ServiceFactory.create(clinic=self.clinic, active=True)
        self.inactive_service = ServiceFactory.create(clinic=self.clinic, active=False)
        self.other_clinic_service = ServiceFactory.create(clinic=self.other_clinic, active=True)

        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        self.validator = ChargeServiceValidator()

    def test_invalid_visit_clinic(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"visit": self.other_visit, "service": self.service}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("visit", context.exception.detail)
        self.assertIn("Invalid visit data", context.exception.detail["visit"])

    def test_invalid_service_clinic(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"visit": self.visit, "service": self.other_clinic_service}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("visit", context.exception.detail)
        self.assertIn("Invalid visit data", context.exception.detail["visit"])

    def test_inactive_service(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"visit": self.visit, "service": self.inactive_service}
        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)
        self.assertIn("visit", context.exception.detail)
        self.assertIn("Invalid visit data", context.exception.detail["visit"])

    def test_valid_charge_service(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"visit": self.visit, "service": self.service}
        try:
            self.validator(attrs, serializer)
        except serializers.ValidationError:
            self.fail("ChargeServiceValidator raised ValidationError unexpectedly!")
