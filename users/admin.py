from django.contrib import admin
from .models import CustomUser, TrainerUser, AthleteUser
from .submodels.relationship import Invitation

admin.site.register(CustomUser)
admin.site.register(TrainerUser)
admin.site.register(AthleteUser)
admin.site.register(Invitation)