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


# chat/consumers.py
from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):


    def message_to_json(self, message):
        return MessageSerializer(message).data

    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))

        return result

    @database_sync_to_async
    def fetch_messages(self, data):
        print("hello world")
        messages = Message.last_30_messages()
        content = {
            'messages' : self.messages_to_json(messages)
        }

        self.send_message(content) 

    @database_sync_to_async
    def new_message(self, data):
        to_user = User.objects.get(pk = data['to'])

        try:
            serializer = MessageSerializer(data={
                "content" : data['message'],
                "attached_file" : data['attached_file'],
                "author" : self.scope['user'].id,
                "to" : data['to']
            })
        except:
            serializer = MessageSerializer(data={
                "content" : data['message'],
                "author" : self.scope['user'].id,
                "to" : data['to']
            })

        

        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        content = {
            'command' : 'new_message',
            'message' : self.message_to_json(message),
        }

        return content

    async def send_chat_message(self, message):
        data = await self.new_message(message)

        await self.chat_message({
            "message" : data
        })

        # Send message to room group
        await self.channel_layer.group_send(
            'chat_' + str(data['message']['to']),
            {
                'type': 'chat_message',
                'message': data
            }
        )

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : send_chat_message
    }


    async def connect(self):
        self.room_name = self.scope['user'].id
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

    

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            message
        ))





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