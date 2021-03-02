from rest_framework.response import Response
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly, TrainersOnly
from utils.exceptions import InvalidCode
from ..serializers.relationship import InvitationCodeSerializer, InvitationCodeViewSerializer
from ..submodels.relationship import InvitationCode
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin 
from trainings.models.diet import Diet
from trainings.models.rutine import Rutine




"""
FIXME: 

CREATE PERMISSION CLASSES 
"""

class InvitationCodeView(ModelViewSet, RetrieveModelMixin, DestroyModelMixin):

    """
        InvitationCodeView():

        Manage invitation code for accept and create.

    """
    serializer_class = InvitationCodeSerializer
    permission_classes = [IsAuthenticated, TrainersOnly]
    
    def get_queryset(self):
        trainer = TrainerUser.objects.get(user = self.request.user)
        query = InvitationCode.objects.filter(trainer= trainer)
        return query


    def list(self, request):
        trainer = TrainerUser.objects.get(user = request.user)
        query = InvitationCode.objects.filter(trainer= trainer)
        serializer = InvitationCodeViewSerializer(query, many = True)
        return Response(serializer.data)

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

    @action(detail=False, methods=['post'], permission_classes=[AllowAny,AthletesOnly])
    def join_trainer(self, request):
        try:
            code = request.data['key']
            code = InvitationCode.objects.get(key = code)

            user = AthleteUser.objects.get(user = request.user)

            user.trainer = code.trainer
            user.trainer_diet = Diet.objects.create(name="Dieta 1", owner=code.trainer)
            user.trainer_rutine =Rutine.objects.create(name="Rutina 1", owner=code.trainer)
            user.rutine =Rutine.objects.create(name="Dieta entrenador 1", owner=code.trainer)
            user.diet = Diet.objects.create(name="Rutina entrenador 1", owner=code.trainer)
            user.save()

            code.delete()

            return Response({"Exito" : "Te has unido a tu entrenador"}, status.HTTP_202_ACCEPTED)
        except:
            raise InvalidCode