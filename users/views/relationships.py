from rest_framework.response import Response
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly, TrainersOnly
from utils.exceptions import InvalidCode
from ..serializers.relationship import InvitationCodeSerializer, InvitationCodeViewSerializer
from ..submodels.relationship import InvitationCode
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny




"""
FIXME: 

CREATE PERMISSION CLASSES 
"""

class InvitationCodeView(ViewSet):

    """
        InvitationCodeView():

        Manage invitation code for accept and create.

    """
    serializer_class = InvitationCodeSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        trainer = TrainerUser.objects.get(user = request.user)
        invCode = InvitationCode.objects.create(trainer=trainer)
        
        data = {
            "code" : invCode.key
        }

        return Response(data, status= status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny,])
    def validate(self, request):
        try:
            code = request.data['key']
            code = InvitationCode.objects.get(key = code)
            serializer = InvitationCodeViewSerializer(code, many=False) 
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        except:
            raise InvalidCode