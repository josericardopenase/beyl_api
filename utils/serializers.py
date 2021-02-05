from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.utils import model_meta

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