"""Users module"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel

# Create your models here.
class CustomUser(AbstractUser, BaseModel):

    """
    CustomUser():

    Custom user to select between beeing trainer or
    athlete.

    """

    USER_TYPES = [ 
        ('Athlete', 'ATH'),
        ('Trainer', 'TRA'),
    ]

    user_type = models.CharField( 
        'Type of users', 
        help_text='Defines if the user is a athlete or a trainer', 
        choices=USER_TYPES,
        default='Athlete',
        max_length=10)



class TrainerUser(BaseModel):
    
    """
    TrainerUser():

    Saves the relationship between CustomUser (out base user)
    and a trainer.

    """

    user = models.ForeignKey(CustomUser, related_name='trainer_user', on_delete=models.CASCADE)




class AthleteUser(BaseModel):

    """
    AthleteUser():

    Saves the relationship between CustomUser (out base user)
    and a athlete.

    """

    user = models.ForeignKey(CustomUser, related_name='athlete_user', on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerUser, related_name='athlete_trainer',
                                     on_delete=models.CASCADE)

    #===================
     #  User training
    #===================

    rutine = models.OneToOneField('trainings.Rutine', related_name='user_rutine', 
                                on_delete=models.CASCADE, help_text="Rutine of the user")
    diet = models.OneToOneField('trainings.Diet', related_name='user_diet', on_delete=models.CASCADE,
                                help_text="Diet of the user")
