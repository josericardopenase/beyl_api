
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import WeightHistoryViewset, GeneralHistoryViewset


#Adding all routes to the urls
router = routers.SimpleRouter()
router.register(r'weight_update', WeightHistoryViewset, basename="weight_update")
router.register(r'general_history', GeneralHistoryViewset, basename="general_history")

urlpatterns = [
    path('', include(router.urls))
]