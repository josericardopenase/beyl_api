from rest_framework import serializers
from ..models.rutine import Rutine, RutineDay, RutineExcersise, RutineGroup, Excersise, ExcersiseTag
from utils.serializers import OrderedSerializer, Base64ImageField, Base64VideoField
from rest_framework.utils import model_meta

from users.models import TrainerUser

class ExcersiseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ExcersiseTag
        fields = ('id', 'name', 'color_primary', 'color_secondary')

class ExcersiseSerializer(serializers.ModelSerializer):

    tags_read = ExcersiseTagSerializer(source='tags', many=True, read_only = True)
    
    image = Base64ImageField(max_length= 10000000, use_url = True)
    video = Base64VideoField(max_length= 10000000, use_url = True, required=False)
    public = serializers.BooleanField(read_only=True)
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Excersise
        fields = ('id', 'name', 'image', 'difficult', 'description', 'muscles', 'video', 'tags', 'public', 'tags_read', 'is_favourite')

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

    def validate_image(self, image):

        KB =  1000538

        if(image.size > KB):
            raise serializers.ValidationError("La imagen debe ser menor de 1 MB")

        return image

    def validate_video(self, image):

        KB =  3000538

        if(image.size > KB):
            raise serializers.ValidationError("La imagen debe ser menor de 3 MB")

        return image


class RutineExcersiseSerializer(OrderedSerializer):
    excersise = ExcersiseSerializer(many=True)

    class Meta:
        model  = RutineExcersise
        fields = ('id', 'group', 'series', 'anotation', 'excersise', 'order')

class RutineGroupSerializer(serializers.ModelSerializer):
    rutine_excersises = RutineExcersiseSerializer(many=True)

    class Meta:
        model = RutineGroup
        fields = ('id', 'name', 'order', 'rutine_excersises')

class RutineDayDetailSerializer(serializers.ModelSerializer):
    rutine_groups = RutineGroupSerializer(many=True)

    class Meta:
        model = RutineDay
        fields = ('id', 'name','rutine_groups')

class RutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RutineDay
        fields = ('id', 'name', 'order')

class RutineSerializer(serializers.ModelSerializer):

    rutine_days = RutineDaySerializer(many=True)

    class Meta:
        model = Rutine
        fields = ('owner', 'name', 'rutine_days')

#============================================
#TRAINER VIEW
#============================================

class RutineGroupNormalSerializer(OrderedSerializer):

    class Meta:
        model = RutineGroup
        fields = ('id', 'name', 'day', 'order')

    def get_queryset(self):
        return self.Meta.model.objects.filter(day=self.initial_data['day'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(day = instance.day)

class RutineDayNormalSerializer(OrderedSerializer):
    class Meta:
        model = RutineDay
        fields = ('id', 'name', 'order', 'rutine')

    def get_queryset(self):
        return self.Meta.model.objects.filter(rutine=self.initial_data['rutine'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(rutine = instance.rutine)
    

class RutineNormalSerializer(OrderedSerializer):

    class Meta:
        model = Rutine
        fields = ('id', 'owner', 'name', 'rutine_days')

class RutineExcersisePostSerializer(OrderedSerializer):
    class Meta:
        model  = RutineExcersise
        fields = ('id', 'group', 'series', 'anotation', 'excersise', 'order')

    def get_queryset(self):
        return self.Meta.model.objects.filter(group=self.initial_data['group'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(group = instance.group)

class RutineExcersisePatchSerializer(OrderedSerializer):
    class Meta:
        model  = RutineExcersise
        fields = ('id', 'group', 'series', 'anotation', 'order')

    def get_queryset(self):
        return self.Meta.model.objects.filter(group=self.initial_data['group'])

    def get_update_queryset(self, instance):
        return self.Meta.model.objects.filter(group = instance.group)