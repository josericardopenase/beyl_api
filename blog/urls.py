from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import ArticleView




#Adding all routes to the urls
router = routers.SimpleRouter()
router.register(r'articles', ArticleView, basename="articles")

urlpatterns = [
    path('', include(router.urls))
]