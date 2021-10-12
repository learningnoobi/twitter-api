from rest_framework.test import APITestCase
from tweets.models import Tweet, Comment
from users.models import User
from chat.models import Message, PrivateChat

class TestChatModel(APITestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com",
            username="test", password="test123")
        
        self.u2 = User.objects.create_user(
            email="test2@gmail.com",
            username="tes22", password="test123")
        self.u3 = User.objects.create_user(
            email="test3@gmail.com",
            username="tes32", password="test1s23")
        self.room1 = PrivateChat.objects.create(
            user1=self.u1,
            user2=self.u2
        )
        self.lastmsg = Message.objects.create(
            room=self.room1,
            sender=self.u1,
            text="first and last"
        )
        self.client.force_authenticate(user=self.u1)


    def test_return_room_if_exists(self):
        room = PrivateChat.objects.create_room_if_none(self.u1,self.u2)
        room_count = PrivateChat.objects.count()
        self.assertEqual(room_count ,1)
        self.assertEqual(room ,self.room1)
    
    def test_create_room_if_none(self):
        room = PrivateChat.objects.create_room_if_none(self.u1,self.u3)
        room_count = PrivateChat.objects.count()
        self.assertEqual(room_count ,2)
    
    def test_private_chat_connect(self):
        connect =self.room1.connect(self.u1)
        self.assertTrue(connect)
        connect =self.room1.connect(self.u1)
        self.assertFalse(connect)
    
    def test_private_chat_disconnect(self):
        is_removed =self.room1.disconnect(self.u1)
        self.assertTrue(is_removed)
        is_removed =self.room1.disconnect(self.u1)
        self.assertTrue(is_removed)
       
    
    def test_last_msg(self):
        msg = self.room1.last_msg()
        self.assertEqual(msg,self.lastmsg)
    
    def test_private_chat_str(self):
        self.assertEqual(str(self.room1),f'Chat : {self.u1} - {self.u2}')
    
    def test_message_str(self):
        self.assertEqual(str(self.lastmsg),f'From <Room - {self.room1}>')
    
    def test_msg_by_room(self):
        messages = Message.objects.by_room(self.room1)
        self.assertEqual(messages.count() ,1)
