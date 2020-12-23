from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import register, login, relationships


router = routers.SimpleRouter()
router.register(r'register', register.UserRegister)
router.register(r'login', login.UserLogin)
router.register(r'invitation', relationships.InvitationView, basename="invitation")

urlpatterns = [
    path('', include(router.urls))
]