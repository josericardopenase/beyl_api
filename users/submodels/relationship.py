""" Membership Module """

from django.db import models
from utils.models import BaseModel

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