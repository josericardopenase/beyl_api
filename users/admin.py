from django.contrib import admin
from .models import CustomUser, TrainerUser, AthleteUser, TrainerPlan
from .submodels.relationship import InvitationCode 
from  .submodels.expo import ExpoPushToken

admin.site.register(CustomUser)
admin.site.register(TrainerUser)
admin.site.register(TrainerPlan)
admin.site.register(AthleteUser)
admin.site.register(InvitationCode)
admin.site.register(ExpoPushToken)