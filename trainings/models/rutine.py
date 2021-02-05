from django.db import models
from ..settings import athlete_model, trainer_model 
from utils.models import BaseModel, OrderedModel
from decimal import *

athlete_model = athlete_model
trainer_model = trainer_model


# Create your models here.
class Excersise(BaseModel):
    """
    Excersise:

    Base excersises that are saved in the db.

    """
    
    CHOICES = (
        (1, "Very easy"),
        (2, "easy"),
        (3, "Medium"),
        (4, "Difficult"),
        (5, "Hardcore")
    )

    public = models.BooleanField()
    owner = models.ForeignKey('users.TrainerUser', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    difficult = models.IntegerField(choices=CHOICES) 
    image = models.ImageField()
    muscles = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(null = True, blank=True)

    def __str__(self):
        return self.name


class Rutine(BaseModel):
    owner = models.ForeignKey(trainer_model, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="New rutine")


class RutineDay(OrderedModel):

    """

    RutineDay:

    A day on a rutine can be monday, day 1 etc... this day have a one to many rel
    with rutine groups.

    """
    rutine = models.ForeignKey(Rutine, on_delete=models.CASCADE, related_name="rutine_days")
    name = models.CharField(max_length=255, default="Día nuevo")

class RutineGroup(OrderedModel):

    """

    RutineGroup:

    Group of excersises that a day can have.

    """

    day = models.ForeignKey(RutineDay, on_delete=models.CASCADE, related_name='rutine_groups')
    name = models.CharField(max_length=255, default ="Grupo nuevo")

class RutineExcersise(OrderedModel):

    """

        RutineExcersise:

        Rutine excersise have a ref to a excersise in de db 
        and information about a especific rutine and hes propieties

    """

    group = models.ForeignKey(RutineGroup, on_delete=models.CASCADE, related_name='rutine_excersises')    
    series = models.CharField(max_length= 400)
    anotation = models.TextField(blank = True)
    excersise = models.ManyToManyField(Excersise, related_name="excersises")
