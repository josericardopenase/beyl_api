
from rest_framework.response import Response
from ..models import CustomUser, AthleteUser, TrainerUser
from ..serializers.profile import ProfileSerializer, AthleteProfileSerializer, AthleteProfileTrainerSerializer, TrainerProfileSerializer, ExpoTokenSerializer
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

    def list(self, request):
        serializer = ProfileSerializer(request.user) 
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def edit(self, request):
        serializer = ProfileSerializer(request.user, data = request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, AthletesOnly])
    def athlete(self, request):
        athlete = AthleteUser.objects.get(user = request.user)
        serializer = AthleteProfileSerializer(athlete) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, AthletesOnly])
    def expoToken(self, request):
        serializer = ExpoTokenSerializer(data = request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, TrainersOnly])
    def trainer(self, request):
        trainer = TrainerUser.objects.get(user = request.user)
        serializer = TrainerProfileSerializer(trainer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class MyAthletesView(ModelViewSet):

    permission_classes = [IsAuthenticated, TrainersOnly]
    query = AthleteUser.objects.all()
    serializer_class = AthleteProfileTrainerSerializer

    def  get_queryset(self):
        Trainer = TrainerUser.objects.get(user = self.request.user)
        return AthleteUser.objects.filter(trainer = Trainer)


