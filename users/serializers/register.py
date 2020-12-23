
from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.validators import UniqueValidator
from trainings.models import *
from rest_framework.authtoken.models import Token

"""
    FIXME: 

    If you use the api without the field user_type
    it gives a server error instead of a json response

"""
class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type']

    def save(self):
        user = CustomUser(
            username=self.validated_data['username'] ,
            email = self.validated_data['email'],
            user_type = self.validated_data['user_type']
        )

        user.set_password(self.validated_data['password']) 

        user.save()

        if(user.user_type == "Athlete"):
            AthleteUser(user=user).save()
        else:
            TrainerUser(user=user).save()

        token = Token.objects.create(user=user) 

        return token, user
