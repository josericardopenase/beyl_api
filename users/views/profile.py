
from rest_framework.response import Response
from ..models import CustomUser, AthleteUser, TrainerUser
from ..serializers.profile import ProfileSerializer, AthleteProfileSerializer
from rest_framework.viewsets import ViewSet
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

    
    @action(detail=False, methods=['get'], permission_classes=[AthletesOnly,])
    def athlete(self, request):
        athlete = AthleteUser.objects.get(user = request.user)
        serializer = AthleteProfileSerializer(athlete) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
