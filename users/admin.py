from django.contrib import admin
from .models import CustomUser, TrainerUser, AthleteUser
from .submodels.relationship import Invitation, InvitationCode

admin.site.register(CustomUser)
admin.site.register(TrainerUser)
admin.site.register(AthleteUser)
admin.site.register(Invitation)
admin.site.register(InvitationCode)