from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework import status 
from ..serializers.diet import DietSerializer, DietDaySerializer, DietGroupSerializer, DietFoodSerializer, DietDayDetailSerializer, FoodSerializer, DietRecipesSerializer
from ..serializers import diet
from ..models.diet import Diet, DietDay, DietFood, DietGroup, Food, DietRecipe, DietRecipeFood, DietRecipe
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
class DietClientView(ViewSet):
    """

    DietClientView:

    View that allows the athletes to see the Diet and Diet day.
    It defines:
        + list: list the Diet with the ids of days
        + retrieve: it takes the id of a day and gives all that day

    """

    serializer_class = DietSerializer
    permission_classes = [permissions.IsAuthenticated, AthleteWithTrainer]

    def list(self, request):
        athlete = AthleteUser.objects.get(user = request.user)
        if(athlete.diet == None):
            raise NoDiet()

        serializer = DietSerializer(athlete.diet)
        return Response(serializer.data)

    def retrieve(self, request, pk = None):
        athlete = AthleteUser.objects.get(user = request.user)

        try:
            queryset = DietDay.objects.get(id=pk, diet=athlete.diet)
        except:
            raise exceptions.NotFound()

        serializer = DietDayDetailSerializer(queryset) 
        return Response(serializer.data)
        


class RecipeView(ViewSet):
    """
        ExcersiseView:

        to see the excersises in the database.
        It adds two methods:
            + list: for listing all excersises publics or of the trainer.
            + retrieve: for taken all excersises that are public or of the trainer.
    """

    serializer_class = DietRecipesSerializer
    queryset = DietRecipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = DietRecipe.objects.all()
        serializer = DietRecipesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk = None):
        try:
            queryset = DietRecipe.objects.get(id=pk)
            serializer = DietRecipesSerializer(queryset, many=False)
            return Response(serializer.data)
        except:
            raise exceptions.NotFound()



class pagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20

class FoodView(ModelViewSet):
    """
        ExcersiseView:

        to see the excersises in the database.
        It adds two methods:
            + list: for listing all excersises publics or of the trainer.
            + retrieve: for taken all excersises that are public or of the trainer.
    """

    pagination_class = pagination
    serializer_class = diet.FoodSerializer
    queryset = Food.objects.all().order_by(Length('name'))
    filter_backends = (filters.SearchFilter, )
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ('name', )

    def get_permissions(self):
        if self.request.method == "POST" or self.request.method == "UPDATE" or self.request.method == "PATCH" or self.request.method == "PUT":
            self.permission_classes = [permissions.IsAdminUser,]
        
        return super(FoodView, self).get_permissions()


class DietView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Diet.objects.all()
    serializer_class = diet.DietNormalSerializer

class DietDayView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = DietDay.objects.all()
    serializer_class = diet.DietDayNormalSerializer
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('diet',)

class DietGroupView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = diet.DietGroupNormalSerializer
    queryset = DietGroup.objects.all()
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('day',)

class DietFoodView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin ,GenericViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = DietFood.objects.all()
    serializer_class = diet.DietFoodPostSerializer
    filter_backends = ( django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ('group',)

    def get_serializer_class(self):

        if self.action == 'update' or self.action == 'partial_update' or self.action == "create":
            return self.serializer_class

        return DietFoodSerializer
        

    def create(self, request, *args, **kwargs):
        serializer = diet.DietFoodPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        serializer = diet.DietFoodSerializer(instance=saved)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)