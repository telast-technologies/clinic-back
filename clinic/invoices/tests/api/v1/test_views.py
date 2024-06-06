from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from clinic.invoices.factories import InvoiceFactory
from clinic.patients.factories import PatientFactory
from clinic.staff.factories import StaffFactory
from clinic.visits.factories import VisitFactory


class InvoiceViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = StaffFactory.create()
        self.visit = VisitFactory.create(
            patient=PatientFactory.create(clinic=self.staff.clinic),
        )
        self.invoice = InvoiceFactory.create(visit=self.visit)

        self.client.force_authenticate(user=self.staff.user)

    def test_valid_retrieve_invoice_list(self):
        # Test retrieving invoice list
        InvoiceFactory.create()

        url = reverse("api:v1:invoices:invoice-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_invalid_retrieve_invoice_detail(self):
        invoice = InvoiceFactory.create()
        # Test retrieving invoice detail
        url = reverse("api:v1:invoices:invoice-detail", kwargs={"pk": invoice.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_retrieve_invoice_detail(self):
        url = reverse("api:v1:invoices:invoice-detail", kwargs={"pk": self.invoice.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice_missing_instance(self):
        # Test updating non-existing invoice instance
        url = reverse("api:v1:invoices:invoice-detail", kwargs={"pk": 9999})  # Non-existing invoice pk
        data = {}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_update_invoice_invalid_data(self):
        # Test updating invoice with valid data
        invoice = InvoiceFactory.create()
        url = reverse("api:v1:invoices:invoice-detail", kwargs={"pk": invoice.pk})
        data = {}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_invoice_valid_data(self):
        # Test updating invoice with valid data
        url = reverse("api:v1:invoices:invoice-detail", kwargs={"pk": self.invoice.pk})
        data = {"tax": 20}

        response = self.client.patch(url, data, format="json")

        self.invoice.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.invoice.tax, 20)
