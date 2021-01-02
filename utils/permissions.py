from rest_framework.permissions import BasePermission
from users.models import AthleteUser, TrainerUser

class AthletesOnly(BasePermission):
    """
    AthletesOnly:

    Allow only athletes to interact with that view
    """
    message = "Solo los atletas tienen permiso para acceder."

    def has_permission(self, request, view):
        return request.user.user_type == "Athlete"

class TrainersOnly(BasePermission):
    """
    TrainersOnly:

    Allow only trainers to interact with that view
    """
    message = "Solo los entrenadores tienen permiso para acceder"

    def has_permission(self, request, view):
        return request.user.user_type == "Trainer"

class AthleteWithTrainer(BasePermission):
    """
    TrainersOnly:

    Allow only trainers to interact with that view
    """
    message = "Aun no tienes entrenador. Agrega a el tuyo a traves de los ajustes"

    def has_permission(self, request, view):
        try:
            athlete = AthleteUser.objects.get(user= request.user)
        except:
            return False

        return athlete.trainer != None
