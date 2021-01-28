from django.shortcuts import render
from .models import Article
from .serializer import ArticleSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

# Create your views here.


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size= 20

class ArticleView(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = LargeResultsSetPagination