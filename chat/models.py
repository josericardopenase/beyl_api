from django.db import models
from utils.models import BaseModel
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Message(BaseModel):

    author = models.ForeignKey(User, related_name="author_messages", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.author.username

    def last_30_messages():
        return Message.objects.order_by('-created').all()[:30]