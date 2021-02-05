
from rest_framework.response import Response
from ..models import CustomUser, AthleteUser, TrainerUser
from ..serializers.profile import ProfileSerializer, AthleteProfileSerializer, AthleteProfileTrainerSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status
from utils.permissions import TrainersOnly, AthletesOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from utils.exceptions import NoRutine
# Create your views here.
class ProfileView(ViewSet):

    permission_classes=[IsAuthenticated,]

    def list(self, request):
        serializer = ProfileSerializer(request.user) 
        return Response(serializer.data)

    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, AthletesOnly])
    def athlete(self, request):
        athlete = AthleteUser.objects.get(user = request.user)
        serializer = AthleteProfileSerializer(athlete) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class MyAthletesView(ModelViewSet):

    permission_classes = [IsAuthenticated, TrainersOnly]
    query = AthleteUser.objects.all()
    serializer_class = AthleteProfileTrainerSerializer

    def  get_queryset(self):
        Trainer = TrainerUser.objects.get(user = self.request.user)
        return AthleteUser.objects.filter(trainer = Trainer)


