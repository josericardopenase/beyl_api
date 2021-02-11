
from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.validators import UniqueValidator
from trainings.models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserLoginSerializer(serializers.Serializer):

    email =  serializers.EmailField() 
    password =  serializers.CharField(max_length=255)  

    def validate(self, data):

        """
        Check credentials
        """
        user = authenticate(email = data['email'], password = data['password'])
        print(user)
        
        if not user:
            raise serializers.ValidationError('Dirección de correo electrónico o contraseña incorrectos')
        if not user.is_verified:
            raise serializers.ValidationError('La cuenta aun no esta activa. Revise el correo.')

        self.context['user'] = user
        return data

    def save(self, user_type):

        """
            saving serializer
        """


        user = self.context['user']

        if user.user_type != user_type:
            raise serializers.ValidationError('Solo los {0}s tienen acceso'.format(user_type))

        token = Token.objects.get_or_create(user = user)

        return token, user