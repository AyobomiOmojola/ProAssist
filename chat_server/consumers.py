import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat_server.models import ChatBody
from django.contrib.auth.models import User


class OnetoOneChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id'] 
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data, bytes_data=None):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']

        await self.save_message(sender, self.room_group_name, message, receiver)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
        



    @database_sync_to_async
    def save_message(self, sender, thread_name, message,receiver):
        ChatBody.objects.create(sender=sender, message=message, thread_name=thread_name)


