
from anymail.message import AnymailMessage
from anymail.message import EmailMessage

def SendEmailWithTemplate(email, template, data):

    message = EmailMessage(
                to=["Nuevo usuario <" + email + ">"],
                 # single recipient...
                # ...multiple to emails would all get the same message
                # (and would all see each other's emails in the "to" header)
            )
    message.template_id = template   # use this Sendinblue template
    message.from_email = None  # to use the template's default sender
    message.merge_global_data = data

    message.send()
