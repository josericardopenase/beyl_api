from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Message, Chat
from drf_extra_fields.fields import Base64FileField
import PyPDF2 
from django.core.files.base import ContentFile
import base64
import six
import uuid
import io


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

class MessageBase64FileField(Base64FileField):
    ALLOWED_TYPES = ['pdf', 'jpg', 'png']
    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'File Content',
            'description': 'Content of the file base64 encoded',
            'read_only': False  # <-- FIX
        }

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
            return 'pdf'
        except: 
            import imghdr

            extension = imghdr.what(filename, decoded_file)
            extension = "jpg" if extension == "jpeg" else extension

            return extension


class MessageSerializer(ModelSerializer):
    attached_file = MessageBase64FileField(required=False, use_url=True)

    class Meta:
        model =  Message
        fields = '__all__'