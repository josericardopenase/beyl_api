from exponent_server_sdk import PushMessage, PushClient

SAVE_RUTINE_NOTIFICATION = {
    "title" : "Rutina actualizada!",
    "body" : "Entra en la aplicación para ver los cambios",
    "data" : {
        "action" : "reloadRutine"
    }
}

SAVE_DIET_NOTIFICATION = {
    "title" : "Dieta actualizada!",
    "body" : "Entra en la aplicación para ver los cambios", 
    "data" : {
        "action" : "reloadDiet"
    }
}



def send_notification(NOTIFICATION, TOKEN):
    try:
        response = PushClient().publish(PushMessage(
                to = TOKEN, 
                title= NOTIFICATION['title'],
                body = NOTIFICATION['body'],
                data = NOTIFICATION['data'],
                
                )
            )
    except: 
        pass