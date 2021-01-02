from django.db import models
from utils.models import BaseModel


class History(BaseModel):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    date = models.DateField('Date of the publication')

    class Meta:
        abstract = True

# Create your models here.`
class SportHistory(History):
    """
    SportHistory():

    HIstorial of the done sports in all time.
    All will have time and date, but some will have also
    distance

    """

    name = models.CharField('Name of the sport', max_length=30)
    time = models.TimeField()
    has_distance = models.BooleanField()
    distance = models.FloatField(blank=True)


class MeasurementHistory(History):
    """
        History of the updated weights
    """
    HISTORY_CHOICES = [
        ('WEIGHT', 'weight'),
        ('HEIGHT', 'height'),
        ('FAT', 'fat'),
    ]

    history_type = models.CharField("Type of history behaviour", choices=HISTORY_CHOICES, max_length=100)
    data = models.FloatField("data")
