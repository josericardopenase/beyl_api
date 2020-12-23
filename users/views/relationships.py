from rest_framework.response import Response
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework import permissions
from utils.permissions import AthletesOnly, TrainersOnly
from ..serializers.relationship import InvitationSerializer, InvitationCreateSerializer, InvitationCodeSerializer, ManageInvitationSerializer
from ..submodels.relationship import Invitation, InvitationCode
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class InvitationView(ViewSet):
    """
    InvitationView:

    Viewset for invitations.
    """

    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated, ]

    def get_invitations(self, user, **kwargs):

        """
        get_invitations():

        Get the invitations taking care if the user
        is a athlete or is a trainer. Returning a set of filters
        passed in kwargs parameter.

        """

        queryset = Invitation.objects.all()

        if user.user_type == "Trainer":
            trainer = TrainerUser.objects.get(user = user)
            queryset = queryset.filter(trainer=trainer)
        else:
            athlete = AthleteUser.objects.get(user = user)
            queryset = queryset.filter(athlete= athlete)

        return queryset.filter(**kwargs)

    def list(self, request):
        queryset = self.get_invitations(request.user, confirmed=False) 
        serializer = InvitationSerializer(queryset, many=True) 
        return Response(serializer.data)

    def create(self, request):
        serializer = InvitationCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        env = serializer.save(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[AthletesOnly])
    def manage_invitation(self, request, pk=None):

        invitation = self.get_invitations(request.user, id=pk).first()
        print(invitation)

        if(invitation == None):
            return Response({"Error" :"You dont have permission"}, status= status.HTTP_401_UNAUTHORIZED)

        serializer = ManageInvitationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(invitation)
        return Response(message, status= 200)



