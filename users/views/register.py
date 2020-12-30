
from rest_framework.response import Response
from ..models import CustomUser
from ..serializers.register import UserRegisterSerializer
from ..serializers.login import UserLoginSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import status 

# Create your views here.
class UserRegisterView(ViewSet):

    queryset = CustomUser.objects.all()
    serializer_class =  UserRegisterSerializer

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        data = {
            'user' : user.username,
            'email' : user.email,
            'token' : token.key
        }

        return Response(data, status=status.HTTP_201_CREATED)
