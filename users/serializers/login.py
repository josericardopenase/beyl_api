
from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.validators import UniqueValidator
from trainings.models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserLoginSerializer(serializers.Serializer):

    username =  serializers.CharField(max_length=255) 
    password =  serializers.CharField(max_length=255)  

    def validate(self, data):
        """
        Check credentials
        """

        user = authenticate(username = data['username'], password = data['password'])
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')

        self.context['user'] = user
        return data

    def save(self):
        """
            saving serializer
        """

        user = self.context['user']
        token = Token.objects.get_or_create(user = user)

        return token, user