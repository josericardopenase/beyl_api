from ..submodels.relationship import InvitationCode, Invitation
from rest_framework.serializers import Serializer,ModelSerializer
from rest_framework import serializers
from ..models import TrainerUser, AthleteUser

class InvitationSerializer(ModelSerializer):

    class Meta:
        model = Invitation
        fields = ('id', 'trainer', 'confirmed' , 'athlete')

class InvitationCreateSerializer(ModelSerializer):

    class Meta:
        model = Invitation
        fields = ('athlete',)

    def validate(self, data):
        athlete = data['athlete']
        
        if athlete.trainer != None:
            raise serializers.ValidationError('Invalid option, the athlete already have a trainer')

        return data


    def save(self, user):
        trainer = TrainerUser.objects.get(user = user)
        athlete = self.validated_data['athlete']
        inv = Invitation.objects.get_or_create(trainer   =  trainer,
                                  athlete   =  athlete,
                                  confirmed =  False)

        return InvitationSerializer(inv[0]).data

class InvitationCodeSerializer(ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = ('key', 'trainer')

class ManageInvitationSerializer(Serializer):
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
        operation = self.validated_data['option'] ,
        print(operation)
        if operation[0] == "accept":
            invitation.confirmed = True
            invitation.save()
            invitation.athlete.trainer = invitation.trainer
            invitation.athlete.save()
            return {"operation" : "accepted"}
        else:
            invitation.delete()
            return {"operation" : "declined"}
