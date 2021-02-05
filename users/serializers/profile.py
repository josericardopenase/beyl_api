from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.validators import UniqueValidator
from trainings.models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class ProfileSerializer(serializers.ModelSerializer):
    class Meta():
        fields = ['email', 'profile_pic', 'first_name', 'last_name']
        model  = CustomUser

class TrainerProfileSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()

    class Meta():
        fields = ['user', ]
        model = TrainerUser

class AthleteProfileSerializer(serializers.ModelSerializer):

    trainer = TrainerProfileSerializer()

    class Meta():
        fields = ['trainer', 'weight', 'height', 'fat']
        model  = AthleteUser

class AthleteProfileTrainerSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()

    class Meta():
        fields = ['id','weight', 'height', 'fat', 'diet', 'user', 'trainer_rutine', 'trainer_diet']
        model  = AthleteUser