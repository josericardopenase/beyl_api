from rest_framework.response import Response
from users.models import AthleteUser
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly
from .serializer import WeightHistorySerializer, GeneralHistorySerializer
from rest_framework.permissions import IsAuthenticated
from .models import WeightHistory, GeneralHistory
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10
# Create your views here.
class WeightHistoryViewset(ViewSet):
    serializer_class = WeightHistorySerializer
    permission_classes = [IsAuthenticated, AthletesOnly]

    def list(self, request):
        """

        REFACTOR THIS PLZ PEPE:

        """
        user = AthleteUser.objects.get(user = request.user)
        return Response({'weight' : str(user.weight)}, status.HTTP_202_ACCEPTED)
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return Response(serializer.data)


class GeneralHistoryViewset(ModelViewSet):
    queryset = GeneralHistory.objects.all()
    serializer_class = GeneralHistorySerializer
    permission_classes = [IsAuthenticated, AthletesOnly]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user = AthleteUser.objects.get(user = self.request.user))
        return query_set
