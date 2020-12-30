from rest_framework import serializers
from ..models.diet import Diet, DietDay, DietFood, DietRecipe, DietRecipeFood, DietGroup, Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'protein', 'carbohydrates', 'fat', 'kcalories', 'portion_weight')

class DietRecipeFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = DietRecipeFood
        fields = ('id', 'food', 'portion_cuantity','portion_unity') 

class DietRecipesSerializer(serializers.ModelSerializer):
    diet_recipe_food = DietRecipeFoodSerializer(many=True)

    class Meta:
        model = DietRecipe
        fields = ('id', 'group', 'name','preparation', 'image', 'diet_recipe_food') 

class DietFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = DietFood
        fields = ('id', 'food', 'portion_cuantity','portion_unity') 

class DietGroupSerializer(serializers.ModelSerializer):
    diet_food = DietFoodSerializer(many=True)
    diet_recipes = DietRecipesSerializer(many=True)
    class Meta:
        model = DietGroup
        fields = ('id', 'name', 'anotation', 'diet_food', 'diet_recipes') 

class DietDayDetailSerializer(serializers.ModelSerializer):
    diet_groups = DietGroupSerializer(many=True)

    class Meta:
        model = DietDay
        fields = ('id', 'name', 'order','anotation', 'diet_groups') 

class DietDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DietDay
        fields = ('id', 'name', 'order','anotation') 

class DietSerializer(serializers.ModelSerializer):
    diet_days = DietDaySerializer(many=True)

    class Meta:
        model = Diet
        fields = ('id', 'owner', 'name', 'description', 'diet_days')
