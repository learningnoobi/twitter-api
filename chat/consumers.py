from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import PrivateChat, Message
from users.models import User
from notifications.models import Notification
from django.db.models import Q


class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.me = self.scope.get('user')

        await self.accept()
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user2 = await sync_to_async(User.objects.get)(username=self.other_username)
        self.private_room = await sync_to_async(PrivateChat.objects.create_room_if_none)(self.me, self.user2)
        self.room_name = f'private_room_{self.private_room.id}'
        print('private room is ', self.private_room.id)
        
        
        await sync_to_async(self.private_room.connect)(self.me)

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
    


    async def receive_json(self, content):
        command = content.get("command", None)
        if command == "private_chat":
            message = content.get("message", None)

            self.newmsg = await sync_to_async(Message.objects.create)(
                room=self.private_room,
                sender=self.me,
                text=message
            )
            await self.message_notice()
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "websocket_message",
                    "text": message,
                    "id": self.newmsg.id,
                    "username": self.newmsg.sender.username,
                    "avatar": self.newmsg.sender.avatar.url,
                    "command": command
                }
            )

        if command == "is_typing":
            print('typing')
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "websocket_typing",
                    "text": content["text"],
                    "command": command,
                    "user": content["user"]
                }
            )

    async def websocket_message(self, event):

        await self.send_json(({
            'id': event["id"],
            'text': event["text"],
            'command': event["command"],
            'sender': {
                "username": event["username"],
                "avatar": event["avatar"],


            }
        }))

    async def websocket_typing(self, event):
        await self.send_json((
            {
                'text': event["text"],
                'command': event["command"],
                'user': event["user"]
            }
        ))

    @database_sync_to_async
    def message_notice(self):
        if not Notification.objects.filter(
            Q(notification_type='M',
              to_user=self.user2,
              from_user=self.me) |
            Q(notification_type='M',
                to_user=self.me,
                from_user=self.user2)

        ).exists():
            Notification.objects.create(
                notification_type='M',
                to_user=self.user2,
                from_user=self.me)

    async def disconnect(self, close_code):
       
        await sync_to_async(self.private_room.disconnect)(self.me)
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

