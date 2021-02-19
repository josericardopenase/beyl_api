from django.db import models
from utils.models import BaseModel
from django.contrib.auth import get_user_model

user = get_user_model()

class ExpoPushToken(BaseModel):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'token')
