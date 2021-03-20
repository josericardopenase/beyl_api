from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import register, login, relationships, profile


#Adding all routes to the urls
router = routers.SimpleRouter()
router.register(r'register_athlete', register.AthleteRegisterView, basename="register_athlete")
router.register(r'register_trainer', register.TrainerRegisterView, basename="register_trainer")
router.register(r'login', login.UserLoginView)
router.register(r'invitation_code', relationships.InvitationCodeView, basename="invitation_code")
router.register(r'profile', profile.ProfileView, basename="invitation_code")
router.register(r'my_athletes', profile.MyAthletesView, basename="my_athletes")

urlpatterns = [
    path('', include(router.urls)),
    path('verify_email/', relationships.AccountVerificationAPIView.as_view())
]