from django.http import response
from users.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import json
from notifications.models import Notification

class TestChatView(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com",
            username="test", password="test123")
        
        self.u2 = User.objects.create_user(
            email="test2@gmail.com",
            username="test2", password="test123")
        self.client.force_authenticate(user=self.u1)

    def test_return_chat_messages(self):
        url=reverse('return_chat_messages',kwargs={"username":"test2"})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_rooms(self):
        url= reverse('get_rooms')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_post_rooms(self):
        url= reverse('get_rooms')
        response = self.client.post(url, {"other_user":"test2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)






