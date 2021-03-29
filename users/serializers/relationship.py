from ..submodels.relationship import InvitationCode
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from ..models import TrainerUser, AthleteUser ,CustomUser
from utils.emails.UserEmails import SendWelcomeEmail
from   .profile import TrainerProfileSerializer
from django.conf import settings
import jwt


class InvitationCodeViewSerializer(ModelSerializer):

    trainer =  TrainerProfileSerializer()

    class Meta:
        model = InvitationCode
        fields = ('key', 'trainer')

class InvitationCodeSerializer(Serializer):
    """

        InvitationCodeSerializer:

        Serializer that shows a invitation code.

    """

    key = serializers.CharField(max_length = 8, min_length = 8)

    def validate(self, data):

        """
            FIXME:

            IT COULD BE A PROBLEM THIS TRY AND EXCEPT. 
        """

        try:
            code =  InvitationCode.objects.get(key = data['key'])
        except:
            raise serializers.ValidationError('This code doesnt exist')
        
        self.context['code'] = code
        return data

    def save(self, user):

        """
        We get the code with that key. We get the athlete of the user.
        And if the athlete does not have a trainer we add the code trainer to athlete
        trainer

        """

        # FIXME: LIMIT THE INVITATION CODES THAT CAN BE MADE
        code = self.context['code']
        athlete = AthleteUser.objects.get(user = user)

        # if the athlete already has a trainer we raise a exception.
        if athlete.trainer != None:
            raise serializers.ValidationError({'Error' : 'You have already a trainer, you cant join other'})
        
        code.delete()
        athlete.trainer = code.trainer
        athlete.save()
        return {"Accepted": "You have join that trainer"}





    
class AccountVerificationSerializer(serializers.Serializer):
    """
    Account verification serializer
    """

    token = serializers.CharField()

    def validate(self, data):

        """
            Verification of jwt
        """
        try:
            payload = jwt.decode(data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        except:
            raise serializers.ValidationError('No se ha podido verificar el email con éxito')
        
        if payload['type'] != "email_confirmation":
            raise serializers.ValidationError('No se ha podido verificar el email con éxito')

        self.context['payload'] = payload

        return data

    def save(self):
        """
            Update users verified status
        """

        payload = self.context['payload']

        user = CustomUser.objects.get(email = payload['email'])

        user.is_verified = True

        SendWelcomeEmail(user.email, user.first_name)
        
        user.save()