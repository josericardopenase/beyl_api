from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from utils.permissions import TrainersOnly, AthletesOnly
from users import models
from users.submodels import expo
from rest_framework import status as st
from exponent_server_sdk import PushMessage, PushClient
from utils.notifications import SAVE_DIET_NOTIFICATION, SAVE_RUTINE_NOTIFICATION, send_notification
from model_clone.utils import create_copy_of_instance
from ..models import rutine
from ..models import diet

import copy



@api_view(['POST'])
@permission_classes([IsAuthenticated, TrainersOnly])
def SaveDietView(request, pk):

    try:

        trainer=models.TrainerUser.objects.get(user = request.user)

        ath = models.AthleteUser.objects.get(id = pk)

        if(ath.trainer != trainer):
            return Response({"detail" : "This athlete is not yours"}, status = st.HTTP_400_BAD_REQUEST)

        #Implement clone behaviour
        #=================================

        # rutine_athlete = ath.rutine 
        # rutine_trainer = ath.trainer_rutine 

        # diet -> dietDays -> dietGroups -> dietFood

        #==================================


        ath_user = ath.user



        pk = ath.diet.pk



        ath.diet = None
        ath.save()



        diet.Diet.objects.get(id = pk).delete()

        nueva_dieta = copy.deepcopy(ath.trainer_diet) 

        nueva_dieta.pk = pk
        nueva_dieta.save()


        for x in diet.DietDay.objects.filter(diet=ath.trainer_diet):
            new_day = copy.deepcopy(x)
            new_day.diet = nueva_dieta
            new_day.pk = None
            new_day.save()

            for y in diet.DietGroup.objects.filter(day=x):
                new_group = copy.deepcopy(y)
                new_group.pk = None
                new_group.day = new_day
                new_group.save()

                for z in diet.DietFood.objects.filter(group=y):
                    new_food = copy.deepcopy(z)
                    new_food.pk = None
                    new_food.group = new_group
                    new_food.save()

        ath.diet = nueva_dieta
        ath.save()
        


        #==================================

        expo_tokens = expo.ExpoPushToken.objects.filter(user= ath_user)

        for x in expo_tokens:
            send_notification(SAVE_DIET_NOTIFICATION, x.token)

        return Response({"success" : "Diet saved!"})

    except:
        return Response({"detail" : "Not found athlete"}, status = st.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, TrainersOnly])
def SaveRutineView(request, pk):

    try:



        trainer=models.TrainerUser.objects.get(user = request.user)

        ath = models.AthleteUser.objects.filter(id = pk).first()

        if(ath.trainer != trainer):
            return Response({"detail" : "This athlete is not yours"}, status = st.HTTP_400_BAD_REQUEST)




        ath_user = ath.user




        #Implement clone behaviour
        #=================================

        # rutine_athlete = ath.rutine 
        # rutine_trainer = ath.trainer_rutine 

        # diet -> dietDays -> dietGroups -> dietFood

        #==================================


        ath_user = ath.user



        rutine_pk = ath.rutine.pk



        ath.rutine = None
        ath.save()



        rutine.Rutine.objects.get(id = rutine_pk).delete()

        nueva_rutina = copy.deepcopy(ath.trainer_rutine) 

        nueva_rutina.pk = rutine_pk
        nueva_rutina.save()


        for x in rutine.RutineDay.objects.filter(rutine=ath.trainer_rutine):
            new_day = copy.deepcopy(x)
            new_day.rutine = nueva_rutina
            new_day.pk = None
            new_day.save()

            for y in rutine.RutineGroup.objects.filter(day=x):
                new_group = copy.deepcopy(y)
                new_group.pk = None
                new_group.day = new_day
                new_group.save()

                for z in rutine.RutineExcersise.objects.filter(group=y):
                    new_excersise = copy.deepcopy(z)
                    new_excersise.pk = None
                    new_excersise.group = new_group
                    new_excersise.save()

                    for w in z.excersise.all():
                        new_excersise.excersise.add(w)

        ath.rutine = nueva_rutina
        ath.save()


        #==================================

        expo_tokens = expo.ExpoPushToken.objects.filter(user= ath_user)

        for x in expo_tokens:
            send_notification(SAVE_RUTINE_NOTIFICATION, x.token)

        return Response({"success" : "Rutine saved!"})

    except:
        return Response({"detail" : "Not found athlete"}, status = st.HTTP_400_BAD_REQUEST)
