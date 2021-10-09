from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import PrivateChat, Message
from users.models import User
from notifications.models import Notification





class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.me = self.scope.get('user')

        await self.accept()
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user2 = await sync_to_async(User.objects.get)(username=self.other_username)
        self.private_room = await sync_to_async(PrivateChat.objects.create_room_if_none)(self.me, self.user2)
        self.room_name = f'private_room_{self.private_room.id}'
        print('private room is ', self.private_room.id)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self, content):
        message = content.get("message", None)
        print('username from client is ',content["username"])
        self.newmsg = await sync_to_async(Message.objects.create)(
            room=self.private_room,
            sender=self.me,
            text=message
        )
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "websocket_message",
                "text": message,
                "id": self.newmsg.id,
                "username":self.newmsg.sender.username,
                "avatar": self.newmsg.sender.avatar.url,
            }
        )

    # @database_sync_to_async
    # def store_message(self, text):
    #     Message.objects.create(
    #         room=self.private_room,
    #         sender=self.me,
    #         text=text
    #     )

    #     Notification.objects.create(
    #         notification_type='M',
    #         to_user=self.user2, from_user=self.me)

    async def websocket_message(self, event):


        await self.send_json(({
            'id': event["id"],
            'text': event["text"],
            'sender': {
                "username": event["username"],
                "avatar": event["avatar"]

            }
        }))

    async def disconnect(self, close_code):
        print('disconnected')
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
