from ..submodels.relationship import InvitationCode
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from ..models import TrainerUser, AthleteUser ,CustomUser
from utils.emails.UserEmails import SendWelcomeEmail, SendAccountChangePasswordEmail
from   .profile import TrainerProfileSerializer
from django.conf import settings
import jwt

class SendRecoverPasswordSerializer(Serializer):
    """
    Account verification serializer
    """

    email = serializers.EmailField()

    def validate(self, data):

        """
            Verification of jwt
        """
        try:
            user = CustomUser.objects.get(email = data['email'])
        except:
            user  = None
        
        self.context['user'] = user

        return data

    def save(self):
        """
            Update users verified status
        """

        user = self.context['user']

        if(user != None):
            SendAccountChangePasswordEmail(user.email, user.first_name)


class PerformRecoverPasswordSerializer(serializers.Serializer):
    """
    Account verification serializer
    """

    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        """
            Verification of jwt
        """
        try:
            payload = jwt.decode(data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        except:
            raise serializers.ValidationError('No se ha podido verificar el email con éxito')
        
        if payload['type'] != "password_change":
            raise serializers.ValidationError('No se ha podido verificar el email con éxito')

        self.context['payload'] = payload

        return data

    def save(self):
        """
            Update users verified status
        """

        payload = self.context['payload']

        user = CustomUser.objects.get(email = payload['email'])
        user.set_password(self.validated_data['password'])
        user.save()
