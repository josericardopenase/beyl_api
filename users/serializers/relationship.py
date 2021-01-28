from ..submodels.relationship import InvitationCode
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from ..models import TrainerUser, AthleteUser 
from   .profile import TrainerProfileSerializer


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





    