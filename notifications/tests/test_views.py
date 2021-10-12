
from users.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from tweets.models import Tweet
from notifications.models import Notification

class TestNotificationView(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com",
            username="test", password="test123")
        
        self.u2 = User.objects.create_user(
            email="test2@gmail.com",
            username="test2", password="test123")
        self.tweet1 = Tweet.objects.create(
            title="first Tweet",
            author=self.u1,
        )
      
        
        self.client.force_authenticate(user=self.u1)

    def test_notification_list(self):
        url=reverse('notification-list')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["noti_count"], None)


    def test_notification_seen(self):
        url= reverse('notification-seen')
        response = self.client.get(url, format="json")
        self.assertEqual(response.data, {'user_seen':True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_notification_delete(self):
        url= reverse('notification-seen')
        Notification.objects.create(
              notification_type='R',
                tweet=self.tweet1,
                to_user=self.u1,
                from_user=self.u2
        )
        response = self.client.post(url, {"notify_id":1})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, {'notification_deleted':True})






