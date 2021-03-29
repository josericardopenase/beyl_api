
from rest_framework.response import Response
from ..models import CustomUser, AthleteUser, TrainerUser
from ..serializers.profile import ProfileSerializer, AthleteProfileSerializer, AthleteProfileTrainerSerializer, TrainerProfileSerializer, ExpoTokenSerializer, ChangePasswordSerializer, AthleteProfilePutSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework import status
from utils.permissions import TrainersOnly, AthletesOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from utils.exceptions import NoRutine
from rest_framework import mixins

# Create your views here.
class ProfileView(mixins.ListModelMixin, GenericViewSet):

    permission_classes=[IsAuthenticated,]
    serializer_class=ProfileSerializer

    def get_serializer_class(self):


        if(self.action == "athlete"):
            return AthleteProfilePutSerializer
        return self.serializer_class

    def list(self, request):
        serializer = ProfileSerializer(request.user) 
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def edit(self, request):
        serializer = ProfileSerializer(request.user, data = request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def change_password(self, request):

        obj = request.user
        serializer = ChangePasswordSerializer(data = request.data) 
        serializer.is_valid(raise_exception=True)

        if not obj.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Contraseña equivocada."]}, status=status.HTTP_400_BAD_REQUEST)

        obj.set_password(serializer.data.get("new_password"))
        obj.save()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        return Response(response)


    @action(detail=False, methods=['get','put'], permission_classes=[IsAuthenticated, AthletesOnly])
    def athlete(self, request):
        athlete = AthleteUser.objects.get(user = request.user)

        if request.method == "GET":
            serializer = AthleteProfileSerializer(athlete) 
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        elif request.method == "PUT":
            serializer = AthleteProfilePutSerializer(athlete ,data = request.data, partial=True) 
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, AthletesOnly])
    def expoToken(self, request):
        try:
            serializer = ExpoTokenSerializer(data = request.data) 
            serializer.is_valid(raise_exception=True)
            serializer.save(request.user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"Error" : "ya existe una persona con ese token"}, status=status.HTTP_400_BAD_REQUEST)

        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, TrainersOnly])
    def trainer(self, request):
        trainer = TrainerUser.objects.get(user = request.user)
        serializer = TrainerProfileSerializer(trainer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class MyAthletesView(ModelViewSet):

    permission_classes = [IsAuthenticated, TrainersOnly]
    query = AthleteUser.objects.all()
    serializer_class = AthleteProfileTrainerSerializer

    def destroy(self, request, pk = None):
        try:

            user = self.get_queryset().get(id = pk)
            user.trainer = None
            user.trainer_rutine = None
            user.trainer_diet = None
            user.diet = None
            user.rutine = None
            user.save()

            return Response({"success" : "Se ha eliminado el atleta correctamente"})

        except:
            return Response({"Adios" : "adios"})

    def  get_queryset(self):
        Trainer = TrainerUser.objects.get(user = self.request.user)
        return AthleteUser.objects.filter(trainer = Trainer)


