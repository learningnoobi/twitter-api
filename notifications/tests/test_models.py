from rest_framework.test import APITestCase
from notifications.models import Notification
from users.models import User
from tweets.models import Tweet


class TestNotiModel(APITestCase):

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

        self.tweet1 = Tweet.objects.create(
            title="first Tweet",
            author=self.u1,
        )

        self.client.force_authenticate(user=self.u1)

    def test_message_str(self):
        notifications = Notification.objects.create(
              notification_type='R',
                tweet=self.tweet1,
                to_user=self.u2,
                from_user=self.u1
        )
        self.assertEqual(str(notifications),f'from {self.u1} to {self.u2}')