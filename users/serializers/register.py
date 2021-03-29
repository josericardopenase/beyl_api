
from rest_framework import serializers
from ..models import CustomUser, TrainerUser, AthleteUser, TrainerPlan
from rest_framework.validators import UniqueValidator
from users.submodels.relationship import InvitationCode
from trainings.models import *
from rest_framework.authtoken.models import Token
from utils.emails.UserEmails import SendAccountVerificationEmail
import secrets

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
    amount_excersise = serializers.CharField()
    alergias = serializers.CharField(allow_blank=True, allow_null=True)

    def validate(self, data):

        try:
            inv = InvitationCode.objects.get(key = data['key'])
            self.context['inv'] = inv
            return data
        except:
            raise serializers.ValidationError('El código ingresado es inválido')

        return data

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
            diet= Diet.objects.create(name="Dieta 1", owner=self.context['inv'].trainer),
            rutine = Rutine.objects.create(name="Rutina 1", owner=self.context['inv'].trainer),
            amount_excersise=self.validated_data['amount_excersise'],
            alergias = self.validated_data['alergias']
        ).save()

        self.context['inv'].delete()

        return token, curruser

class TrainerRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField( validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(max_length=40)
    name = serializers.CharField(max_length= 20)
    surname = serializers.CharField(max_length=50 )

    def validate(self, data):
        return data

    def createTestAthlete(self, trainer, name, surname, weight, height, sex, sport):


        num = secrets.token_hex(7)

        while(len(CustomUser.objects.filter(email = "email_de_ejemplo" + num + "@beylapp.com")) != 0):
            num = secrets.token_hex(7)

        user = CustomUser(
            email = "email_de_ejemplo" + num + "@beylapp.com",
            user_type = "Athlete",
            first_name = name,
            last_name = surname,
            is_active = False,
            is_verified = False
        )

        user.save()

        profile = AthleteUser(
            trainer = trainer,
            user = user,
            weight = weight,
            height = height,
            fat = 40,
            born_date = "1995-12-04",
            sexo =  sex,
            trainer_diet= Diet.objects.create(name="Dieta 1", owner=trainer),
            trainer_rutine = Rutine.objects.create(name="Rutina 1", owner=trainer),
            diet= Diet.objects.create(name="Dieta 1", owner=trainer),
            rutine = Rutine.objects.create(name="Rutina 1", owner=trainer),
            amount_excersise= sport,
            alergias = "Ninguna"
        ).save()

    def save(self):

        curruser = CustomUser(
            email=self.validated_data['email'] ,
            user_type = 'Trainer',
            first_name = self.validated_data['name'],
            last_name = self.validated_data['surname'],
            is_active = True,
            is_verified=False
        )

        curruser.set_password(self.validated_data['password'])
        curruser.save()

        profile = TrainerUser(
            user = curruser,
            plan = TrainerPlan.objects.first()
        )



        profile.save()

        self.createTestAthlete(profile, "Jose", "Francisco Pérez", 180, 70, "hombre", "EF")
        self.createTestAthlete(profile, "Paula", "García Hume", 65, 170, "mujer", "EL")
        token = Token.objects.create(user=curruser) 

        SendAccountVerificationEmail(self.validated_data['email'], self.validated_data['name'])

        return token, curruser

