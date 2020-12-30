from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from ..serializers.rutine import RutineSerializer, RutineDaySerializer, RutineGroupSerializer, RutineExcersiseSerializer, RutineDayDetailSerializer, ExcersiseSerializer
from ..models.rutine import Rutine, RutineDay, RutineExcersise, RutineGroup, Excersise
from rest_framework import permissions
from utils.permissions import AthleteWithTrainer
from users.models import AthleteUser, TrainerUser
from rest_framework import exceptions
from utils.exceptions import NoRutine, NoTrainer

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
        


class ExcersiseView(ViewSet):
    """
        ExcersiseView:

        to see the excersises in the database.
        It adds two methods:
            + list: for listing all excersises publics or of the trainer.
            + retrieve: for taken all excersises that are public or of the trainer.
    """

    serializer_class = ExcersiseSerializer
    queryset = Excersise.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Excersise.objects.all().filter(public = True)
        serializer = ExcersiseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk = None):
        try:
            queryset = Excersise.objects.get(id=pk, public = True)
            serializer = ExcersiseSerializer(queryset, many=False)
            return Response(serializer.data)
        except:
            raise exceptions.NotFound()