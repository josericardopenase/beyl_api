from rest_framework import serializers
from ..models.diet import Diet, DietDay, DietFood, DietRecipe, DietRecipeFood, DietGroup, Food
from utils.serializers import OrderedSerializer
from users.models import TrainerUser


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'protein', 'carbohydrates', 'fat', 'kcalories', 'portion_weight', 'tags', 'public')

    def create(self, validated_data):
        user = TrainerUser.objects.get(user = self.context['request'].user)
        instance = super().create(validated_data)
        instance.public = False
        instance.owner = user
        instance.save()
        return instance


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
        fields = ('id', 'food', 'portion_cuantity','portion_unity', 'group', 'order') 

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

#============================================
#TRAINER VIEW
#============================================

class DietGroupNormalSerializer(OrderedSerializer):

    class Meta:
        model = DietGroup
        fields = ('id', 'name', 'day', 'order')

    def get_queryset(self):
        return self.Meta.model.objects.filter(day=self.initial_data['day'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(day = instance.day)

class DietDayNormalSerializer(OrderedSerializer):
    class Meta:
        model = DietDay
        fields = ('id', 'name', 'diet', 'order')

    def get_queryset(self):
        return self.Meta.model.objects.filter(diet=self.initial_data['diet'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(diet = instance.diet)
    

class DietNormalSerializer(OrderedSerializer):
    class Meta:
        model = Diet
        fields = ('id', 'owner', 'name', 'diet_days')

class DietFoodPostSerializer(OrderedSerializer):
    class Meta:
        model  = DietFood
        fields = ('id', 'group', 'portion_cuantity', 'portion_unity', 'food', 'order')

    def get_queryset(self):
        return self.Meta.model.objects.filter(group=self.initial_data['group'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(group = instance.group)
