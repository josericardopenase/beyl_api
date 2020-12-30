from rest_framework.response import Response
from ..models import CustomUser
from ..serializers.login import UserLoginSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import status
from utils.permissions import TrainersOnly
# Create your views here.
class UserLoginView(ViewSet):

    queryset = CustomUser.objects.all()
    serializer_class =  UserLoginSerializer

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        data = {
            'user' : user.username,
            'email' : user.email,
            'token' : token[0].key
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)

    
