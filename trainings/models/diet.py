from django.db import models
from ..settings import athlete_model, trainer_model
from utils.models import BaseModel

athlete_model = athlete_model
trainer_model = trainer_model

# Create your models here.
class Food(BaseModel):
    name = models.CharField(max_length=255)
    protein = models.IntegerField() 
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()
    kcalories = models.IntegerField()
    portion_weight = models.IntegerField() 

    def __str__(self):
        return self.name

class Diet(BaseModel):
    owner = models.ForeignKey(trainer_model, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Dieta nueva")
    description = models.TextField(null=True, blank=True)

class DietDay(BaseModel):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='diet_days')
    name = models.CharField(max_length=255,default="Dia nuevo")
    order = models.IntegerField()
    anotation = models.TextField(null=True, blank=True)

class DietGroup(BaseModel):
    day = models.ForeignKey(DietDay, on_delete=models.CASCADE, related_name='diet_groups')
    name = models.CharField(max_length=255, default="Grupo nuevo")
    anotation = models.TextField(null=True, blank=True)

class DietFood(BaseModel):
    CHOICES = (
        ("gr", "gramos"),
        ("oz", "oz"),
        ("unity", "unity"),
    )

    group = models.ForeignKey(DietGroup, on_delete=models.CASCADE, related_name='diet_food')    
    portion_cuantity = models.IntegerField(default=100)
    portion_unity = models.CharField(choices=CHOICES, default=0, max_length=14)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

class DietRecipe(BaseModel):
    group = models.ForeignKey(DietGroup, on_delete=models.CASCADE, related_name= 'diet_recipes')    
    name = models.CharField(max_length=255, default="Nueva receta")
    preparation = models.TextField()
    image = models.ImageField()

class DietRecipeFood(BaseModel):

    CHOICES = (
        ("gr", "gramos"),
        ("oz", "oz"),
        ("unity", "unity"),
    )

    recipe = models.ForeignKey(DietRecipe, on_delete=models.CASCADE, related_name="diet_recipe_food")
    portion_cuantity = models.IntegerField()
    portion_unity = models.CharField(choices=CHOICES, default=0, max_length=14)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
