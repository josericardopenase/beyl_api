from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Message, Chat

class ChatSerializer(ModelSerializer):

    other =  SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'

    def get_other(self, obj):
        user = self.context['request'].user
        if(user.pk == obj.user_1.pk):
            return obj.user_2
        
        return obj.user_1


class MessageSerializer(ModelSerializer):
    class Meta:
        model =  Message
        fields = '__all__'