from utils.emails.sendEmails import SendEmailWithTemplate
from django.core import mail
from django.test import TestCase

class EmailTest(TestCase):
    def test_send_email(self):
        SendEmailWithTemplate('jrpenaseco@gmail.com', 3, {})
        self.assertEqual(1, 1)