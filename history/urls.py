
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import WeightHistoryViewset, GeneralHistoryViewset, WeightHistoryGlobal


#Adding all routes to the urls
router = routers.SimpleRouter()
router.register(r'weight_update', WeightHistoryViewset, basename="weight_update")
router.register(r'general_history', GeneralHistoryViewset, basename="general_history")
router.register(r'weight_history', WeightHistoryGlobal, basename="weight_history_trainer")

urlpatterns = [
    path('', include(router.urls))
]