from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import status 
from ..serializers.rutine import RutineSerializer, RutineDaySerializer, RutineGroupSerializer, RutineExcersiseSerializer, RutineDayDetailSerializer, ExcersiseSerializer, RutineNormalSerializer, RutineDayNormalSerializer, RutineGroupNormalSerializer, RutineExcersisePostSerializer, RutineExcersisePatchSerializer

from ..models.rutine import Rutine, RutineDay, RutineExcersise, RutineGroup, Excersise
from rest_framework import permissions
from utils.permissions import AthleteWithTrainer
from users.models import AthleteUser, TrainerUser
from rest_framework import exceptions
from utils.exceptions import NoRutine, NoTrainer
from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework
from rest_framework import filters
from rest_framework import mixins
from django.db.models.functions import Length
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

class ExcersiseView(ModelViewSet):
    """
        ExcersiseView:

        to see the excersises in the database.
        It adds two methods:
            + list: for listing all excersises publics or of the trainer.
            + retrieve: for taken all excersises that are public or of the trainer.
    """

    pagination_class = pagination
    serializer_class = ExcersiseSerializer
    queryset = Excersise.objects.all().order_by(Length('name'))
    filter_backends = (filters.SearchFilter, )
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ('name', )

    def get_permissions(self):
        if self.request.method == "POST" or self.request.method == "UPDATE" or self.request.method == "PATCH" or self.request.method == "PUT":
            self.permission_classes = [permissions.IsAdminUser,]
        
        return super(ExcersiseView, self).get_permissions()

class RutineView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Rutine.objects.all()
    serializer_class = RutineNormalSerializer

class RutineDayView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = RutineDay.objects.all()
    serializer_class = RutineDayNormalSerializer
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('rutine',)

class RutineGroupView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = RutineGroup.objects.all()
    serializer_class = RutineGroupNormalSerializer
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('day',)

class RutineExcersiseView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin ,GenericViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = RutineExcersise.objects.all()
    serializer_class = RutineExcersiseSerializer
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('group',)

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update': 
            return RutineExcersisePatchSerializer

        return self.serializer_class 
        

    def create(self, request, *args, **kwargs):
        serializer = RutineExcersisePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        serializer = self.get_serializer(instance=saved)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
