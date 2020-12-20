from django.db import models
from ..settings import athlete_model, trainer_model

athlete_model = athlete_model
trainer_model = trainer_model

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    protein = models.IntegerField() 
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()
    kcalories = models.IntegerField()
    portion_weight = models.IntegerField() 

    def __str__(self):
        return self.name

class Diet(models.Model):
    owner = models.ForeignKey(trainer_model, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    anotation = models.TextField(null=True, blank=True)

class DietDay(models.Model):
    rutine = models.ForeignKey(Diet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    anotation = models.TextField(null=True, blank=True)

class DietGroup(models.Model):
    day = models.ForeignKey(DietDay, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    anotation = models.TextField(null=True, blank=True)

class DietFood(models.Model):
    CHOICES = (
        (0, "gr"),
        (1, "oz"),
        (2, "unity"),
    )

    group = models.ForeignKey(DietGroup, on_delete=models.CASCADE)    
    portion_cuantity = models.IntegerField()
    portion_unity = models.IntegerField(choices=CHOICES)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

class DietRecipe(models.Model):
    group = models.ForeignKey(DietGroup, on_delete=models.CASCADE)    
    name = models.CharField(max_length=255)
    preparation = models.TextField()
    image = models.ImageField()

class DietRecipeFood(models.Model):

    CHOICES = (
        (0, "gr"),
        (1, "oz"),
        (2, "unity"),
    )

    recipe = models.ForeignKey(DietRecipe, on_delete=models.CASCADE)
    group = models.ForeignKey(DietGroup, on_delete=models.CASCADE)    
    portion_cuantity = models.IntegerField()
    portion_unity = models.IntegerField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

