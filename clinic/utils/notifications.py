from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from notifications.signals import notify

from clinic.users.models import User


def send_email(recipient_list, subject, message):
    msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    msg.send()


def send_inbox(sender, recipient_list, title, message, *args, **kwargs):
    recipient = User.objects.filter(email__in=recipient_list)
    notify.send(sender, recipient=recipient, verb=title, description=message)
