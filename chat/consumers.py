# chat/consumers.py
from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncJsonWebsocketConsumer
from .models import Message, Chat
from channels.db import database_sync_to_async
import json
from rest_framework.authtoken.models import Token
from random import randint
from .serializers import MessageSerializer
from time import sleep
from asgiref.sync import async_to_sync


User = get_user_model()

""" class ChatConsumer(AsyncWebsocketConsumer):


    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content' : message.content,
            'timestamp' : str(message.created)
        }

    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))

        return result

    @database_sync_to_async
    def fetch_messages(self, data):
        messages = Message.last_30_messages()
        content = {
            'messages' : self.messages_to_json(messages)
        }

        self.send_message(content) 

    @database_sync_to_async
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(author= self.scope['user'], content=data['message'])
        
        content = {
            'command' : 'new_message',
            'message' : self.message_to_json(message),
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    

    async def send_chat_message(self, message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            message
        })) """


""" class IntegerWsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "room1"
        self.room_group_name = 'room1'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        
    async def receive(self, *, text_data):
            await self.channel_layer.group_send(self.room_group_name, {"type" : "chat_message" , "message" : json.loads(text_data)['message']})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data = json.dumps({
            'message' : message,
            'author' : self.scope['user'].email
        })) """


class ChatConsumer(AsyncJsonWebsocketConsumer):


    @database_sync_to_async
    def chat_to_json(self):
        """
            Get all the chats from a client.
        """
        pass

    @database_sync_to_async
    def message_to_json(self, text_data):
        """
        pass massege to json format using
        drf serializers
        """

        data = json.loads(text_data)
        data['author'] = self.scope['user'].pk
        serializer = MessageSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        return MessageSerializer(model).data


    async def send_chat_message(self, data):
        pass


    async def send_chats(self, data):
        pass


    commands = {
        "get_chats" : send_chats,
        "send_message" : send_chat_message,
    }

    async def connect(self):
        """
            Connects the user with chat service
            and takes care that the user must be logged
        """

        if(self.scope['user'].is_anonymous):
            self.close()
        else:
            print(self.scope['user'].pk)
            self.room_name = str(self.scope['user'].pk)
            self.room_group_name = str(self.scope['user'].pk)
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()

    async def receive(self, *, text_data):
        """
            Receive data with a concrete command
            and execute the service rutine of that 
            command.
        """

        data = json.loads(text_data) 
        command = data['command']
        del data['command']
        self.commands[command](self, data)

    async def send_room_message(self, data):
        """

        """
        await self.channel_layer.group_send(str(data['to']), {
            "type"     : "send_message",
            "message"  : data
        })

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data = json.dumps({
            **message
        })) 

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.room_group_name)
        await self.close()






"""             await self.channel_layer.group_send(self.room_group_name, {"type" : "chat_message" , "message" : json.loads(text_data)['message']}) """




"""
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if(self.scope['user'].is_anonymous):
            self.close()
        else:
            print(self.scope['user'].pk)
            self.room_name = str(self.scope['user'].pk)
            self.room_group_name = str(self.scope['user'].pk)
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.room_group_name)
        await self.close()

    async def notify(self, event):
        await self.send(text_data=json.dumps(event['text']))
"""