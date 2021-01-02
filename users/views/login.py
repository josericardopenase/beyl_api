from rest_framework.response import Response
from ..models import CustomUser
from ..serializers.login import UserLoginSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import status
from utils.permissions import TrainersOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from utils.exceptions import NoRutine
# Create your views here.
class UserLoginView(ViewSet):

    queryset = CustomUser.objects.all()
    serializer_class =  UserLoginSerializer

    @action(detail=False, methods=['post'], permission_classes=[])
    def athletes(self, request):
        serializer = UserLoginSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save("Athlete")
        

        data = {
            'profile_image' : user.profile_pic.url,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'token' : token[0].key
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)

    


    @action(detail=False, methods=['post'], permission_classes=[])
    def trainers(self, request):
        serializer = UserLoginSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save("Trainer")

        data = {
            'profile_image' : user.profile_pic.url,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'token' : token[0].key
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)
