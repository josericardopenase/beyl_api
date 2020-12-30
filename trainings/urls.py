
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views.rutine import RutineClientView, ExcersiseView
from .views.diet import DietClientView, RecipeView

router = routers.SimpleRouter()
router.register(r'rutine_client', RutineClientView, basename="rutines_client")
router.register(r'excersise', ExcersiseView, basename="rutines_client")
router.register(r'diet_client', DietClientView, basename="diet_client")
router.register(r'recipe', RecipeView, basename="diet_client")

urlpatterns = [
    path('', include(router.urls))
]