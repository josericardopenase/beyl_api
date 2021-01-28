from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework import status 
from ..serializers.rutine import RutineSerializer, RutineDaySerializer, RutineGroupSerializer, RutineExcersiseSerializer, RutineDayDetailSerializer, ExcersiseSerializer, RutineNormalSerializer, RutineDayNormalSerializer, RutineGroupNormalSerializer

from ..models.rutine import Rutine, RutineDay, RutineExcersise, RutineGroup, Excersise
from rest_framework import permissions
from utils.permissions import AthleteWithTrainer
from users.models import AthleteUser, TrainerUser
from rest_framework import exceptions
from utils.exceptions import NoRutine, NoTrainer
from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework
from rest_framework import filters

class RutineClientView(ViewSet):
    """

    RutineClientView:

    View that allows the athletes to see the Rutine and rutine day.
    It defines:
        + list: list the rutine with the ids of days
        + retrieve: it takes the id of a day and gives all that day

    """

    serializer_class = RutineSerializer
    permission_classes = [permissions.IsAuthenticated, AthleteWithTrainer]

    def list(self, request):
        athlete = AthleteUser.objects.get(user = request.user)
        if(athlete.rutine == None):
            raise NoRutine()
        serializer = RutineSerializer(athlete.rutine)
        return Response(serializer.data)

    def retrieve(self, request, pk = None):
        athlete = AthleteUser.objects.get(user = request.user)
        try:
            queryset = RutineDay.objects.get(id=pk, rutine=athlete.rutine)
        except:
            raise exceptions.NotFound()

        serializer = RutineDayDetailSerializer(queryset) 
        return Response(serializer.data)
        

class pagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20

class ExcersiseView(ReadOnlyModelViewSet):
    """
        ExcersiseView:

        to see the excersises in the database.
        It adds two methods:
            + list: for listing all excersises publics or of the trainer.
            + retrieve: for taken all excersises that are public or of the trainer.
    """

    pagination_class = pagination
    serializer_class = ExcersiseSerializer
    queryset = Excersise.objects.all()
    filter_backends = (filters.SearchFilter, )
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ('name', )

class RutineView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Rutine.objects.all()
    serializer_class = RutineNormalSerializer

class RutineDayView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = RutineDay.objects.all()
    serializer_class = RutineDayNormalSerializer

class RutineGroupView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = RutineGroup.objects.all()
    serializer_class = RutineGroupNormalSerializer

class RutineExcersiseView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = RutineExcersise.objects.all()
    serializer_class = RutineExcersiseSerializer

