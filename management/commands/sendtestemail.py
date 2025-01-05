from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends a test email to the specified recipient(s)'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+', type=str, help='Email address(es) to send the test email to')

    def handle(self, *args, **kwargs):
        subject = 'Test Email'
        message = 'This is a test email from Django.'
        from_email = settings.EMAIL_HOST_USER  # Get email address from settings.py
        recipient_list = kwargs['email']

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS('Successfully sent test email to %s' % ', '.join(recipient_list)))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to send test email: %s' % str(e)))
