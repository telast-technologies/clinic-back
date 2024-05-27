from django.conf import settings
from django.core import mail
from django.test import TestCase

from clinic.users.factories import UserFactory
from clinic.utils.notifications import send_email, send_inbox


class NotificationTest(TestCase):
    def setUp(self):
        self.recipient_email = "elhaatem@gmail.com"
        self.recipient = UserFactory.create(email=self.recipient_email)
        self.recipient_list = [self.recipient_email]
        self.subject = "Test Subject"
        self.message = "This is a test message"
        self.title = "Test Title"

    def test_send_email(self):
        send_email(self.recipient_list, self.subject, self.message)
        # Check that EmailMultiAlternatives was initialized correctly
        mailoutbox = mail.outbox
        self.assertEqual(len(mailoutbox), 1)
        self.assertEqual(mailoutbox[0].subject, self.subject)
        self.assertEqual(mailoutbox[0].body, self.message)
        self.assertEqual(mailoutbox[0].to, self.recipient_list)
        self.assertEqual(mailoutbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_send_inbox(self):
        send_inbox(sender=self.recipient, recipient_list=self.recipient_list, title=self.title, message=self.message)

        # Check that notify.send was called with the correct arguments
        self.assertEqual(self.recipient.notifications.count(), 1)
