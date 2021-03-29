from rest_framework.response import Response
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly, TrainersOnly
from utils.exceptions import InvalidCode
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin 
from trainings.models.diet import Diet
from trainings.models.rutine import Rutine
from rest_framework.views import APIView
from ..serializers.recover import SendRecoverPasswordSerializer, PerformRecoverPasswordSerializer

class SendRecoverPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendRecoverPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Si el correo es correcto, se ha enviado un email para realizar el cambio solicitado.'}
        return Response(data, status.HTTP_200_OK)

class PerformRecoverPassword(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PerformRecoverPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Cambio de contraseña realizado con éxito'}
        return Response(data, status.HTTP_200_OK)