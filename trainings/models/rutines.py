from django.db import models
from ..settings import athlete_model, trainer_model 
athlete_model = athlete_model
trainer_model = trainer_model


# Create your models here.
class Excersise(models.Model):
    CHOICES = (
        (1, "Very easy"),
        (2, "easy"),
        (3, "Medium"),
        (4, "Difficult"),
        (5, "Hardcore")
    )

    name = models.CharField(max_length=255)
    difficult = models.IntegerField(choices=CHOICES) 
    image = models.ImageField()
    description = models.TextField()

class Rutine(models.Model):
    owner = models.ForeignKey(trainer_model, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class RutineDay(models.Model):
    rutine = models.ForeignKey(Rutine, on_delete=models.CASCADE, related_name="days")
    name = models.CharField(max_length=255)
    order = models.IntegerField()

class RutineGroup(models.Model):
    day = models.ForeignKey(RutineDay, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)
    order = models.IntegerField()

class RutineExcersise(models.Model):
    group = models.ForeignKey(RutineGroup, on_delete=models.CASCADE, related_name='excersises')    
    series = models.CharField(max_length= 400)
    anotation = models.TextField()
    excersise = models.ManyToManyField(Excersise)
    order = models.IntegerField()
