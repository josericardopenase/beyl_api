"""Users module"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel
from datetime import date
from django.utils.timezone import now
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
        max_length=10, 
        blank=False)

    USERNAME_FIELD = 'email'

    is_verified = models.BooleanField("User verified", default=False,
                                      help_text="Have user confirmed hes email?")
    email = models.EmailField('email address', blank=False, unique=True)
    profile_pic = models.ImageField(blank=False, default='profile.png')
    first_name = models.CharField(blank=False, max_length=58)
    last_name = models.CharField(blank=False, max_length=58)
    username = models.CharField(blank=True, null=True, max_length=50)
    REQUIRED_FIELDS = []


class TrainerUser(BaseModel):

    """
    TrainerUser():

    Saves the relationship between CustomUser (out base user)
    and a trainer.

    """

    user = models.ForeignKey(CustomUser, related_name='trainer_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class AthleteUser(BaseModel):

    """
    AthleteUser():

    Saves the relationship between CustomUser (out base user)
    and a athlete.

    """
    
    SEX_CHOICES = ( 
        ('H','Hombre'), 
        ('M','Mujer'),
        ('O','Otro'),
    )

    user = models.ForeignKey(CustomUser, related_name='athlete_user', on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerUser, related_name='athlete_trainer',
                                     on_delete=models.CASCADE, null=True, blank=True)

    #===================
     #  User training
    #===================

    rutine = models.OneToOneField('trainings.Rutine', related_name='user_rutine',
                                on_delete=models.CASCADE, help_text="Rutine of the user", blank=True, null=True)
    diet = models.OneToOneField('trainings.Diet', related_name='user_diet', on_delete=models.CASCADE,
                                help_text="Diet of the user", blank=True, null=True)

    weight = models.FloatField('weight', help_text="Weight of the user in Kg")
    height = models.FloatField('height', help_text="Hieght of the user in Cm")
    fat = models.FloatField('fat_percent', help_text="Fat in percentage")
    born_date = models.DateField()
    sexo = models.CharField('sex_choices', help_text="Choices of sex", choices=SEX_CHOICES, max_length=8)
    alergias = models.ManyToManyField('trainings.Food')

    def __str__(self):
        return self.user.username