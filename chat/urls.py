from .views import MessageViewset
from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'chat', MessageViewset, basename="message_viewset")


urlpatterns = [
    path('', include(router.urls)),
]