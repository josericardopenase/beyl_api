
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
    """
    Serializer for the registration method.
    It gives a
        + username
        + password
        + email
        + user_type

    """

    class Meta:

        """
         Class meta for the model serializer 
        """
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type']

    def save(self):
        """
            if all fields are valid we create a new username with that data
            and we set hes password. Also depending if its an athlete or a trainer
            we create a athlete profile and a trainer profile
        """
        # We create a user
        user = CustomUser(
            username=self.validated_data['username'] ,
            email = self.validated_data['email'],
            user_type = self.validated_data['user_type']
        )

        # We set users password
        user.set_password(self.validated_data['password']) 

        # We save that user
        user.save()

        # if its a athlete we create a athlete user
        if(user.user_type == "Athlete"):
            AthleteUser(user=user).save()
        # if its a trainer we create a trainer user
        else:
            TrainerUser(user=user).save()

        # We create a token for that user to login
        token = Token.objects.create(user=user) 

        #We return the token and the user
        return token, user
