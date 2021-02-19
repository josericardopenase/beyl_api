
from rest_framework.response import Response
from ..models import CustomUser
from ..serializers.register import UserRegisterSerializer, AthleteRegisterSerializer,TrainerRegisterSerializer
from ..serializers.login import UserLoginSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.decorators import action
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


class TrainerRegisterView(ViewSet):

    serializer_class =  TrainerRegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        data = {
            'email' : user.email,
            'token' : token.key
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[])
    def verify_email(self, request):
        email = request.data['email']

        if email is None:
            return Response({'error' : 'you need to set a valid email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email = email)
            return Response({'error' : 'this email already exist'}, status= status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'success' : 'this email is valid'}, status=status.HTTP_200_OK)


        
