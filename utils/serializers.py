from rest_framework.serializers import ModelSerializer, Serializer, ImageField, FileField
from rest_framework.utils import model_meta


class Base64VideoField(FileField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
            

        return super(Base64VideoField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

        return "mp4"

class Base64ImageField(ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
            

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class OrderedSerializer(ModelSerializer):

    class Meta:
        model = None
        queryset = None

    def get_queryset(self):
        pass

    def get_update_queryset(self, instance):
        pass

    def create(self, validated_data):
        """
        We define the order
        """
        try:
           validated_data['order'] = self.get_queryset().last().order + 1 
        except:
            validated_data['order'] = 1

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)

        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        instance = self.Meta.model.objects.create(**validated_data)

        if many_to_many: 
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)
            
        return instance
        

    def update(self, instance, validated_data):

        try:
            instance.move_to(self.get_update_queryset(instance), validated_data['order'])
            validated_data['order'] = instance.order
            instance = super(OrderedSerializer, self).update(instance, validated_data)
        except:
            instance = super(OrderedSerializer, self).update(instance, validated_data)

        return instance