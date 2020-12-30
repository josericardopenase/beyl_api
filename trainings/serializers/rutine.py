from rest_framework import serializers
from ..models.rutine import Rutine, RutineDay, RutineExcersise, RutineGroup, Excersise

class ExcersiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excersise
        fields = ('id', 'name', 'image', 'difficult', 'description', 'muscles', 'video')

class RutineExcersiseSerializer(serializers.ModelSerializer):
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