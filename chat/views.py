from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response

# Create your views here.
@api_view(['post'])
@permission_classes([IsAuthenticated])
def enviar_notificacion(request):
    channel_layer = get_channel_layer()
    data = "Mira que guapa la notificacion"
    print(request.user.pk)
    async_to_sync(channel_layer.group_send)(
        str(request.user.pk),
        {
            "type" : "notify",
            "text" : data
        }
    )

    return Response("perfecto")
