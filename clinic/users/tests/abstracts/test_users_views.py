from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL="http://ui.com/password/reset/confirm")
class PasswordResetConfirmRedirectTestCase(TestCase):
    def test_password_reset_redirect(self):
        # Generate a dummy uidb64 and token
        uidb64 = "dummy_uidb64"
        token = "dummy_token"
        # Construct the expected redirect URL
        expected_redirect_url = f"http://ui.com/password/reset/confirm/{uidb64}/{token}/"
        # Generate the URL for the view
        url = f"/api/auth/password/reset/confirm/{uidb64}/{token}/"
        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the response is a redirect
        self.assertIsInstance(response, HttpResponseRedirect)
        # Check that the redirect URL matches the expected URL
        self.assertEqual(response.url, expected_redirect_url)
