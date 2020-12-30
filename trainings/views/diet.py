from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from ..serializers.diet import DietSerializer, DietDaySerializer, DietGroupSerializer, DietFoodSerializer, DietDayDetailSerializer, FoodSerializer, DietRecipesSerializer
from ..models.diet import Diet, DietDay, DietFood, DietGroup, Food, DietRecipe, DietRecipeFood, DietRecipe
from rest_framework import permissions
from utils.permissions import AthleteWithTrainer
from users.models import AthleteUser, TrainerUser
from rest_framework import exceptions
from utils.exceptions import NoDiet, NoTrainer

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