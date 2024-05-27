from django.test import TestCase

from clinic.approvals.choices import JoinRequestStatusChoices
from clinic.approvals.factories import JoinRequestFactory
from clinic.approvals.forms import JoinRequestForm


class JoinRequestFormTest(TestCase):
    def test_readonly_status_when_not_pending(self):
        # Create a JoinRequest instance with status other than PENDING
        join_request = JoinRequestFactory.create(status=JoinRequestStatusChoices.APPROVED)

        # Initialize the form with the created instance
        form = JoinRequestForm(instance=join_request)

        # Check that the 'status' field is readonly and disabled
        self.assertTrue(form.fields["status"].widget.attrs.get("readonly"))
        self.assertTrue(form.fields["status"].disabled)

    def test_status_editable_when_pending(self):
        # Create a JoinRequest instance with status PENDING
        join_request = JoinRequestFactory.create(status=JoinRequestStatusChoices.PENDING)

        # Initialize the form with the created instance
        form = JoinRequestForm(instance=join_request)

        # Check that the 'status' field is editable
        self.assertFalse(form.fields["status"].widget.attrs.get("readonly"))
        self.assertFalse(form.fields["status"].disabled)

    def test_invalid_form_data(self):
        # Test form validation with invalid data
        invalid_data = {"status": "INVALID_STATUS"}  # Invalid status choice
        form = JoinRequestForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("status" in form.errors)

    def test_missing_form_data(self):
        # Test form validation with missing data
        form = JoinRequestForm(data={})  # Empty data dictionary
        self.assertFalse(form.is_valid())
        self.assertTrue("status" in form.errors)
