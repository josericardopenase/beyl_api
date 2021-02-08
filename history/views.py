from rest_framework.response import Response
from users.models import AthleteUser, TrainerUser
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly , TrainersOnly
from .serializer import WeightHistorySerializer, GeneralHistorySerializer, GeneralHistoryTrainerSerializer, WeightHistoryTrainerSerializer
from rest_framework.permissions import IsAuthenticated
from .models import WeightHistory, GeneralHistory
from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework
from rest_framework import filters
from rest_framework import mixins

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
    permission_classes = [IsAuthenticated,]
    pagination_class = LargeResultsSetPagination
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('user',)

    def get_serializer_class(self):
        if self.action == 'list':
            return GeneralHistoryTrainerSerializer

        return self.serializer_class 

    def get_queryset(self):
        queryset = self.queryset

        if(self.request.user.user_type == "Trainer"):
            query_set = queryset.filter(user__in = AthleteUser.objects.filter(trainer = TrainerUser.objects.get(user=self.request.user)))
        else:
            query_set = queryset.filter(user = AthleteUser.objects.get(user = self.request.user))

        return query_set



class WeightHistoryGlobal(ReadOnlyModelViewSet):
    queryset = WeightHistory.objects.all()
    serializer_class = WeightHistoryTrainerSerializer
    permission_classes = [IsAuthenticated, TrainersOnly]
    pagination_class = LargeResultsSetPagination
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('user',)

    def get_queryset(self):
        queryset = self.queryset

        query_set = queryset.filter(user__in = AthleteUser.objects.filter(trainer = TrainerUser.objects.get(user=self.request.user)))

        return query_set
