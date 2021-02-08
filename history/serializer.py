from .models import WeightHistory, GeneralHistory
from rest_framework.serializers import ModelSerializer
from users.models import AthleteUser
from users.serializers.profile import ProfileSerializer, AthleteProfileTrainerSerializer
from rest_framework import serializers


class WeightHistorySerializer(ModelSerializer):
    """
    Serializesr of wewight history, you need only the data and be athlete.

    """
    class Meta():
        model = WeightHistory
        fields = ('data',)

    def validated(self, data):
        """
        validated():

        if the weight is less than 0 or bigger than 3000
        we raise a exeption

        """
        weight = data['data']

        if weight < 0 or weight > 300:
            raise serializers.ValidationError('Peso invalido, tiene que ser menor a 300 kg y mayor a 0kg')

        return data

    def save(self, user):
        """
        save:

        we save the weight history and update the weight of the user
        """

        weight = self.validated_data['data']
        athlete = AthleteUser.objects.get(user = user)
        athlete.weight = weight 
        athlete.save()

        w_hist = WeightHistory.objects.create(user =  athlete, data=weight)


class GeneralHistorySerializer(ModelSerializer):
    """
    Serializesr of wewight history, you need only the data and be athlete.

    """
    class Meta():
        model = GeneralHistory
        fields = ('date', 'name', 'time', 'has_distance', 'distance',)

    def validated(self, data):
        """
        validated():

        if the weight is less than 0 or bigger than 3000
        we raise a exeption

        """
        has_distance = data['data']
        distance = data['distance']

        if has_distance and distance == None: 
            raise serializers.ValidationError('Es necesario agregar una distancia.')

        if distance < 0: 
            raise serializers.ValidationError('Ponga una distancia válida')

        return data

    def save(self):
        """
        save:

        we save the weight history and update the weight of the user
        """

        athlete = AthleteUser.objects.get(user = self.context['request'].user)


        GeneralHistory.objects.create(
            user = athlete,
            date = self.validated_data['date'],
            name = self.validated_data['name'],
            time = self.validated_data['time'],
            has_distance = self.validated_data['has_distance'],
            distance = self.validated_data['distance'],

        )





class GeneralHistoryTrainerSerializer(ModelSerializer):
    """
    Serializesr of wewight history, you need only the data and be athlete.
    """

    user = AthleteProfileTrainerSerializer()

    class Meta():
        model = GeneralHistory
        fields = ('date', 'name', 'time', 'has_distance', 'distance', 'user')

class WeightHistoryTrainerSerializer(ModelSerializer):
    """
    Serializesr of wewight history, you need only the data and be athlete.

    """
    class Meta():
        model = WeightHistory
        fields = ('data', 'user', 'created')