from django.test import RequestFactory, TestCase
from clinic.healthcare.factories import ServiceFactory
from clinic.invoices.factories import InvoiceFactory
from rest_framework import serializers

from clinic.inventory.factories import SupplyFactory
from clinic.invoices.api.v1.serializers import ChargeServiceModifySerializer, CreateChargeItemSerializer
from clinic.invoices.api.validators import ChargeItemValidator, ChargeServiceValidator
from clinic.patients.factories import PatientFactory
from clinic.staff.factories import StaffFactory
from clinic.system_management.factories import ClinicFactory
from clinic.visits.factories import VisitFactory


class ChargeItemValidatorTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.other_clinic = ClinicFactory.create(name="Other Clinic")

        self.staff = StaffFactory.create(clinic=self.clinic)
        self.patient = PatientFactory.create(clinic=self.clinic)
        self.other_patient = PatientFactory.create(clinic=self.other_clinic)

        self.visit = VisitFactory.create(patient=self.patient)
        self.other_visit = VisitFactory.create(patient=self.other_patient)

        self.invoice = InvoiceFactory.create(visit=self.visit)
        self.other_invoice = InvoiceFactory.create(visit=self.other_visit)
        
        self.supply = SupplyFactory.create(clinic=self.clinic, quantity=10)
        self.other_supply = SupplyFactory.create(clinic=self.other_clinic, quantity=10)

        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        self.validator = ChargeItemValidator()

    def test_invalid_visit_clinic(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"invoice": self.other_invoice, "supply": self.supply, "quantity": 1}
        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("invoice", context.exception.detail)
        self.assertIn("Invalid invoice data", context.exception.detail["invoice"])

    def test_invalid_supply_clinic(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"invoice": self.invoice, "supply": self.other_supply, "quantity": 1}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("invoice", context.exception.detail)
        self.assertIn("Invalid invoice data", context.exception.detail["invoice"])

    def test_insufficient_supply(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"invoice": self.invoice, "supply": self.supply, "quantity": 11}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("invoice", context.exception.detail)
        self.assertIn("Invalid invoice data", context.exception.detail["invoice"])

    def test_valid_charge_item(self):
        serializer = CreateChargeItemSerializer(context={"request": self.request})
        attrs = {"invoice": self.invoice, "supply": self.supply, "quantity": 5}

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

        self.invoice = InvoiceFactory.create(visit=self.visit)
        self.other_invoice = InvoiceFactory.create(visit=self.other_visit)
        
        self.service = ServiceFactory.create(clinic=self.clinic, active=True)
        self.inactive_service = ServiceFactory.create(clinic=self.clinic, active=False)
        self.other_clinic_service = ServiceFactory.create(clinic=self.other_clinic, active=True)

        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        self.validator = ChargeServiceValidator()

    def test_invalid_visit_clinic(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"invoice": self.other_invoice, "service": self.service}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("invoice", context.exception.detail)
        self.assertIn("Invalid invoice data", context.exception.detail["invoice"])

    def test_invalid_service_clinic(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"invoice": self.invoice, "service": self.other_clinic_service}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)

        self.assertIn("invoice", context.exception.detail)
        self.assertIn("Invalid invoice data", context.exception.detail["invoice"])

    def test_inactive_service(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"invoice": self.invoice, "service": self.inactive_service}
        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)
        self.assertIn("invoice", context.exception.detail)
        self.assertIn("Invalid invoice data", context.exception.detail["invoice"])

    def test_valid_charge_service(self):
        serializer = ChargeServiceModifySerializer(context={"request": self.request})
        attrs = {"invoice": self.invoice, "service": self.service}
        try:
            self.validator(attrs, serializer)
        except serializers.ValidationError:
            self.fail("ChargeServiceValidator raised ValidationError unexpectedly!")
