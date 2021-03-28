from rest_framework import serializers
from ..models.diet import Diet, DietDay, DietFood, DietRecipe, DietRecipeFood, DietGroup, Food, FoodTag
from utils.serializers import OrderedSerializer
from users.models import TrainerUser
from rest_framework.utils import model_meta


class FoodTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTag
        fields = ('id','name', 'color_primary', 'color_secondary')

class FoodSerializer(serializers.ModelSerializer):
    tags_read = FoodTagSerializer(source='tags', many=True, read_only=True)
    public = serializers.BooleanField(read_only=True)
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ('id', 'name', 'protein', 'carbohydrates', 'fat', 'kcalories', 'portion_weight', 'tags', 'public', 'tags_read', 'is_favourite')
        read_only_fields = ('public', 'id')
    
    def get_is_favourite(self, obj):
        user = self.context['request'].user
        trainer = TrainerUser.objects.get(user = user)
        return obj.favourites.filter(pk = trainer.pk).exists()


    def create(self, validated_data):
        #clean the validated_data
        owner = TrainerUser.objects.get(user = self.context['request'].user)
        validated_data['owner']  = TrainerUser.objects.get(user = self.context['request'].user)
        validated_data['public'] = False
        return  super().create(validated_data)

    def update(self, instance,  validated_data):
        if(instance.public == True):
            raise serializers.ValidationError("No puedes modificar un ejericio publico")
        return super().update(instance, validated_data)
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
