from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import RetrieveModelMixin

class pagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MessageViewset(GenericViewSet, RetrieveModelMixin):
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes  = [IsAuthenticated]
    pagination_class = pagination

    def get_queryset(self):
        return super().get_queryset()

    def retrieve(self, request, pk=None):

        user =  request.user

        try:
            to = get_user_model().objects.get(pk = pk)
        except: 
            return Response({"Error" : "No se ha encontrado el usuario solicitado"}, status= status.HTTP_400_BAD_REQUEST)

        query = Message.objects.filter(Q(to=user, author=to) | Q(to=to, author = user))
        page = self.paginate_queryset(query)

        if page is not None: 
            serializer = self.get_serializer(page, many= True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)
