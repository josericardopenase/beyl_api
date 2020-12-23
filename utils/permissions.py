from rest_framework.permissions import BasePermission

class AthletesOnly(BasePermission):
    """
    AthletesOnly:

    Allow only athletes to interact with that view
    """
    message = "Only athletes have access to this view"

    def has_permission(self, request, view):
        return request.user.user_type == "Athlete"

class TrainersOnly(BasePermission):
    """
    TrainersOnly:

    Allow only trainers to interact with that view
    """
    message = "Only trainers have access to this view"

    def has_permission(self, request, view):
        return request.user.user_type == "Trainer"
