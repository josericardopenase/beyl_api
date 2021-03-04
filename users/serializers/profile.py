from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser, TrainerPlan
from rest_framework.validators import UniqueValidator
from trainings.models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ..submodels.expo import ExpoPushToken
from PIL import Image
from utils.serializers import Base64ImageField
class ProfileSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(max_length= 10000000, use_url = True)
    class Meta():
        fields = ['email', 'profile_pic', 'first_name', 'last_name']
        model  = CustomUser

    def validate_profile_pic(self, image):

        KB =  1000538

        if(image.size > KB):
            raise serializers.ValidationError("La imagen debe ser menor de 1 MB")

        return image



class ExpoTokenSerializer(serializers.ModelSerializer):
    class Meta():
        fields = ['token']
        model  = ExpoPushToken

    def save(self, user):
        expoToken = ExpoPushToken(
            user = user,
            token = self.validated_data['token']
        )

        expoToken.save()

        return expoToken

        


class TrainerPlanSerializer(serializers.ModelSerializer):
    class Meta():
        fields = ['user_count', 'name']
        model = TrainerPlan

class TrainerProfileSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()
    plan = TrainerPlanSerializer()


    class Meta():
        fields = ['user', 'plan']
        model = TrainerUser

class AthleteProfileSerializer(serializers.ModelSerializer):

    trainer = TrainerProfileSerializer()

    class Meta():
        fields = ['trainer', 'id','weight', 'height', 'fat', 'diet', 'user', 'trainer_rutine', 'trainer_diet', 'born_date', 'age', 'sexo', 'amount_excersise', 'alergias']
        model  = AthleteUser

class AthleteProfilePutSerializer(serializers.ModelSerializer):

    class Meta():
        fields = ['height', 'born_date', 'age', 'sexo', 'amount_excersise', 'alergias']
        model  = AthleteUser

class AthleteProfileTrainerSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()

    class Meta():
        fields = ['id','weight', 'height', 'fat', 'diet', 'user', 'trainer_rutine', 'trainer_diet', 'born_date', 'age', 'sexo', 'amount_excersise', 'alergias']
        model  = AthleteUser

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)