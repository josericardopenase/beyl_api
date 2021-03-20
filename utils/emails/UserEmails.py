from .sendEmails import SendEmailWithTemplate
import jwt  
from django.conf import settings

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
