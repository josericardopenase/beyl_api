from django.db import models
from utils.models import BaseModel
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Chat(BaseModel):

    """

    A chat is a object that makes a relation between
    two users.

    """

    user_1 = models.ForeignKey(User, null = False, on_delete=models.CASCADE, related_name='user_1')
    user_2 = models.ForeignKey(User, null = False, on_delete=models.CASCADE, related_name='user_2')

class Message(BaseModel):
    """
        Message class that represents a chat messege. It has a owner, 
        a to (which is the user who the message was sended), and timestamp,
        also a attached file.

    """

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat', null = True, blank = True)

    author = models.ForeignKey(User, related_name="author_messages", on_delete=models.CASCADE, null = False, blank = False)

    to = models.ForeignKey(User, related_name="receiver_messages", on_delete=models.CASCADE, null = False, blank = False)

    content = models.TextField(null=False, blank=False)

    attached_file = models.FileField(null = True, blank = True)


    def other(self, user):
        if(type(user) is User):
            if(self.to == user):
                return self.author
            return self.to

        return None


    def __str__(self):
        return str(self.content)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.content)

    def notify_ws_clients(self):
        """
        Send a notification to client that there is a new message.
        """
        pass 


    class Meta:
        ordering = ('-created',)