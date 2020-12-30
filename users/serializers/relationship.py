from ..submodels.relationship import InvitationCode, Invitation
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from ..models import TrainerUser, AthleteUser 

class InvitationSerializer(ModelSerializer):

    """
    Invitation serializer:

    Serializer to show invitations.
    """

    class Meta:
        model = Invitation
        fields = ('id', 'trainer', 'confirmed' , 'athlete')

class InvitationCreateSerializer(ModelSerializer):

    """
    InvitationCreateSerializer:

    Serialilzer to handle creating a invitation.

    """

    class Meta:
        """
            We set the model serializer values
        """
        model = Invitation
        fields = ('athlete',)

    def validate(self, data):
        """
            If the athlete already have 
            a trainer, we show a exception.

        """
        athlete = data['athlete']
        
        if athlete.trainer != None:
            raise serializers.ValidationError('Invalid option, the athlete already have a trainer')

        return data


    def save(self, user):
        """

            We create the invitation returning it.
            If that invitation already exist we get the one
            that exist.

        """

        trainer = TrainerUser.objects.get(user = user)
        athlete = self.validated_data['athlete']
        inv = Invitation.objects.get_or_create(trainer   =  trainer,
                                  athlete   =  athlete,
                                  confirmed =  False)

        return InvitationSerializer(inv[0]).data

class ManageInvitationSerializer(Serializer):
    """

        Serializer to manage invitations.
        You can select accept or decline depending on the 
        invitation.

    """
    option = serializers.CharField(max_length = 10)

    def validate(self, data):

        """
        Check valid option
        """

        option = data['option']
        
        if option != "accept" and option != "decline":
            raise serializers.ValidationError('Invalid option, must be : accept or decline')

        return data

    def save(self, invitation):
        """

         If operation is accept we add that trainer
         to the athlete. Else we remove the invitation.

        """
        # get the operation to do
        operation = self.validated_data['option'] 

        #if its accept we make the athlete trainer equals to the invitation trainer.
        if operation[0] == "accept":
            invitation.athlete.trainer = invitation.trainer
            invitation.confirmed = True
            invitation.athlete.save()
            return {"operation" : "accepted"}
        #else we delete the invitation
        else:
            invitation.delete()
            return {"operation" : "declined"}

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





    