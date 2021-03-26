from rest_framework import serializers
from ..models.rutine import Rutine, RutineDay, RutineExcersise, RutineGroup, Excersise
from utils.serializers import OrderedSerializer, Base64ImageField, Base64VideoField

from users.models import TrainerUser

class ExcersiseSerializer(serializers.ModelSerializer):

    image = Base64ImageField(max_length= 10000000, use_url = True)
    video = Base64VideoField(max_length= 10000000, use_url = True)
    class Meta:
        model = Excersise
        fields = ('id', 'name', 'image', 'difficult', 'description', 'muscles', 'video', 'tags', 'public')

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
    def create(self, validated_data):
        user = TrainerUser.objects.get(user = self.context['request'].user)
        print(user)
        validated_data['public'] = False
        instance = super().create(validated_data)
        instance.public = False
        instance.owner = user
        instance.save()
        return instance
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