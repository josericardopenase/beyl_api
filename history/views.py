from rest_framework.response import Response
from users.models import AthleteUser
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly
from .serializer import WeightHistorySerializer, GeneralHistorySerializer
from rest_framework.permissions import IsAuthenticated
from .models import WeightHistory, GeneralHistory

# Create your views here.
class WeightHistoryViewset(ViewSet):
    serializer_class = WeightHistorySerializer
    permission_classes = [IsAuthenticated, AthletesOnly]

    def list(self, request):
        user = AthleteUser.objects.get(user = request.user)
        return Response({'weight' : str(user.weight)}, status.HTTP_202_ACCEPTED)
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return Response(serializer.data)


class GeneralHistoryViewset(ViewSet):
    serializer_class = GeneralHistorySerializer
    permission_classes = [IsAuthenticated, AthletesOnly]

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return Response(serializer.data)