from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import register, login, relationships


router = routers.SimpleRouter()
router.register(r'register', register.UserRegisterView)
router.register(r'login', login.UserLoginView)
router.register(r'invitation', relationships.InvitationView, basename="invitation")
router.register(r'invitation_code', relationships.InvitationCodeView, basename="invitation_code")

urlpatterns = [
    path('', include(router.urls))
]