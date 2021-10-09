from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async


class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')

        self.me = user.username
        print(self.me)
        await self.accept()

        self.room_name = f'love_{self.me}'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self, content):
        message = content.get("message", None)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "websocket_message",
                "text": message

            }
        )

    async def send_status(self, event):
        print('sent status')
        await self.send_json({'payload': event})
        print(event)

    async def websocket_message(self, event):

        await self.send_json(({
            'message': event["text"],
            'user': self.me
        }))

    async def disconnect(self, close_code):
        print('disconnected')
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

