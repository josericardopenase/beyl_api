
from rest_framework.response import Response
from ..models import CustomUser
from ..serializers.register import UserRegisterSerializer, AthleteRegisterSerializer
from ..serializers.login import UserLoginSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import status 


# Create your views here.
class AthleteRegisterView(ViewSet):

    serializer_class =  AthleteRegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        data = {
            'email' : user.email,
            'token' : token.key
        }

        return Response(data, status=status.HTTP_201_CREATED)

