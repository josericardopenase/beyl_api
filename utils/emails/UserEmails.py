from .sendEmails import SendEmailWithTemplate
import jwt  
from django.conf import settings
import django.utils.timezone
from datetime import timedelta
from django.utils import timezone

def SendRegisterEmail(email, nombre):
    SendEmailWithTemplate(email, 12, {"name" : nombre})

def SendWelcomeEmail(email, nombre):
    SendEmailWithTemplate(email, 11, {"name" : nombre, "email" : email})

def SendAccountVerificationEmail(email, nombre):
    payload = {
        "email" : email,
        "type" : "email_confirmation"
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    SendEmailWithTemplate(email, 12 ,{"name" : nombre, "link" : str(token)})


def SendAccountChangePasswordEmail(email, nombre):
    exp_date = timezone.now() + timedelta(seconds = 1400)

    payload = {
        "email" : email,
        "type" : "password_change",
        "exp" : exp_date
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    SendEmailWithTemplate(email, 13 ,{"name" : nombre, "link" : str(token)})