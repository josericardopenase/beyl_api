from django.db import models
from ..settings import athlete_model, trainer_model
from utils.models import BaseModel, OrderedModel
from model_clone import mixins

athlete_model = athlete_model
trainer_model = trainer_model

# Create your models here.

class FoodTag(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Food(BaseModel):
    name = models.CharField(max_length=255)
    public = models.BooleanField(default=False, db_column='is_public', blank=True)
    owner = models.ForeignKey(trainer_model, null=True, blank=True, db_column='trainer_owner', on_delete=models.CASCADE)
    tags = models.ManyToManyField(FoodTag, db_table='trainings_food_tags', blank=True)
    protein = models.FloatField() 
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    kcalories = models.FloatField()
    portion_weight = models.FloatField() 

    def __str__(self):
        return self.name


class Diet(mixins.CloneMixin ,BaseModel):

    owner = models.ForeignKey(trainer_model, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Dieta nueva")
    description = models.TextField(null=True, blank=True)

class DietDay(OrderedModel):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='diet_days')
    name = models.CharField(max_length=255,default="Dia nuevo")

    order = models.IntegerField(default = 10)
    anotation = models.TextField(default = "")

class DietGroup(OrderedModel):

    day = models.ForeignKey(DietDay, on_delete=models.CASCADE, related_name='diet_groups')
    name = models.CharField(max_length=255, default="Grupo nuevo")
    anotation = models.TextField(null=True, blank=True)

class DietFood(OrderedModel):

    CHOICES = (
        ("gr", "gramos"),
        ("oz", "oz"),
        ("unity", "unity"),
    )

    group = models.ForeignKey(DietGroup, on_delete=models.CASCADE, related_name='diet_food')    
    portion_cuantity = models.IntegerField(default=100)
    portion_unity = models.CharField(choices=CHOICES, default=0, max_length=14)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

class DietRecipe(OrderedModel):
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

