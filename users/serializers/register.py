
from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser
from rest_framework.validators import UniqueValidator
from users.submodels.relationship import InvitationCode
from trainings.models import *
from rest_framework.authtoken.models import Token

"""
    FIXME: 

    If you use the api without the field user_type
    it gives a server error instead of a json response

"""
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for the registration method.
    It gives a
        + username
        + password
        + email
        + user_type

    """

    class Meta:

        """
         Class meta for the model serializer 
        """
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type']

    def save(self):
        """
            if all fields are valid we create a new username with that data
            and we set hes password. Also depending if its an athlete or a trainer
            we create a athlete profile and a trainer profile
        """
        # We create a user
        user = CustomUser(
            username=self.validated_data['username'] ,
            email = self.validated_data['email'],
            user_type = self.validated_data['user_type']
        )

        # We set users password
        user.set_password(self.validated_data['password']) 

        # We save that user
        user.save()

        # if its a athlete we create a athlete user
        if(user.user_type == "Athlete"):
            AthleteUser(user=user).save()
        # if its a trainer we create a trainer user
        else:
            TrainerUser(user=user).save()

        # We create a token for that user to login
        token = Token.objects.create(user=user) 

        #We return the token and the user
        return token, user

class AthleteRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField( validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(max_length=40)
    name = serializers.CharField(max_length= 20)
    surname = serializers.CharField(max_length=50 )
    height = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    key = serializers.CharField()
    born_date = serializers.DateField()

    def validate(self, data):

        try:
            inv = InvitationCode.objects.get(key = data['key'])
            self.context['inv'] = inv
            return data
        except:
            raise serializers.ValidationError('El código ingresado es inválido')

    def save(self):

        curruser = CustomUser(
            email=self.validated_data['email'] ,
            user_type = 'Athlete',
            first_name = self.validated_data['name'],
            last_name = self.validated_data['surname'],
            is_active = True,
            is_verified=True
        )

        curruser.set_password(self.validated_data['password']) 

        curruser.save()

        print(curruser)

        token = Token.objects.create(user=curruser) 

        profile = AthleteUser(
            trainer = self.context['inv'].trainer,
            user = curruser,
            weight = self.validated_data['weight'],
            height = self.validated_data['height'],
            fat = self.validated_data['height'],
            born_date = self.validated_data['born_date'],
            sexo =  self.validated_data['sex'],
            trainer_diet= Diet.objects.create(name="Dieta 1", owner=self.context['inv'].trainer),
            trainer_rutine = Rutine.objects.create(name="Rutina 1", owner=self.context['inv'].trainer),
        ).save()

        self.context['inv'].delete()

        return token, curruser



