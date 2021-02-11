""" Membership Module """

from django.db import models
from utils.models import BaseModel
import random
import string

class InvitationCode(BaseModel):

    """
    InvitationCode:

    Invitation link for a athlete join a 
    trainer.

    """

    key = models.CharField("key", max_length=8, primary_key=True, unique=True, blank=True)
    trainer = models.ForeignKey('users.TrainerUser', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
        return result_str

    def __str__(self):
        return self.key
