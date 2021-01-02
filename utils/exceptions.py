from rest_framework.exceptions import APIException

class NoRutine(APIException):
    status_code = 403
    default_detail = 'Tu rutina no esta disponible, espera que tu entrenador la termine.'
    default_code = 'no_rutine'

class NoTrainer(APIException):
    status_code = 403
    default_detail = 'No tienes un entrenador asignado. Agrega a tu entrenador.'
    default_code = 'no_trainer'

class NoDiet(APIException):
    status_code = 403
    default_detail = 'Tu dieta no esta disponible, espera que tu entrenador la termine.'
    default_code = 'no_diet'