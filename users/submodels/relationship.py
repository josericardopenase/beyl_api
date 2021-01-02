""" Membership Module """

from django.db import models
from utils.models import BaseModel
import random
import string

class Invitation(BaseModel):
    """
    AthleteTrainerRelationship

    is a table that holds the relationship between athlete
    and trainers
    """

    trainer = models.ForeignKey('users.TrainerUser', on_delete=models.CASCADE)
    athlete = models.ForeignKey('users.AthleteUser', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    """
        - Agregar el plan que tiene contratado el usuario
    """

    def __str__(self):
        """ return trainer and athlete"""
        return '@{} is trainer of @{}'.format(
            self.trainer,
            self.athlete
        )

class InvitationCode(BaseModel):

    """
    InvitationCode:

    Invitation link for a athlete join a 
    trainer.

    """

    key = models.CharField("key", max_length=8, primary_key=True, unique=True)
    trainer = models.ForeignKey('users.TrainerUser', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
        return result_str

    def __str__(self):
        return self.key
