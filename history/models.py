from django.db import models
from utils.models import BaseModel


class History(BaseModel):
    user = models.ForeignKey('users.AthleteUser', on_delete=models.CASCADE)

    class Meta:
        """
        
        We make the class abstract and set a default 
        ordering.

        """
        abstract = True
        get_latest_by = ['-created',]
        ordering = ('-created',)

# Create your models here.`
class GeneralHistory(History):
    """
    SportHistory():

    HIstorial of the done sports in all time.
    All will have time and date, but some will have also
    distance

    """

    date = models.DateField('Date of the publication')
    name = models.CharField('Name of the sport', max_length=30)
    time = models.TimeField()
    has_distance = models.BooleanField()
    distance = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ("-date",)


class WeightHistory(History):
    """
        History of the updated weights
    """

    add_date = models.DateField('Date of the publication', auto_now=True)
    data = models.FloatField("data")
