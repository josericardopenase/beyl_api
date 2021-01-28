
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import rutine
from .views import diet

router = routers.SimpleRouter()
router.register(r'rutine_client', rutine.RutineClientView, basename="rutines_client")
router.register(r'excersise', rutine.ExcersiseView, basename="rutines_client")
router.register(r'diet_client', diet.DietClientView, basename="diet_client")
router.register(r'recipe', diet.RecipeView, basename="diet_client")
router.register(r'rutine', rutine.RutineView)
router.register(r'rutine_day', rutine.RutineDayView)
router.register(r'rutine_group', rutine.RutineGroupView)
router.register(r'rutine_excersise', rutine.RutineExcersiseView)



urlpatterns = [
    path('', include(router.urls))
]