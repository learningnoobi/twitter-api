from django.test import TestCase
from tweets.models import Tweet, Comment
from .models import User
# Create your tests here.
import logging

class TestTweetModel(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com",
            username="test", password="test123")
        self.u2 = User.objects.create_superuser(
            email="test2@gmail.com",
            username="test2", password="test123")

    def test_superuser_or_normal_user(self):
        self.assertTrue(self.u2.is_superuser)
        self.assertFalse(self.u1.is_superuser)
        self.assertEqual(self.u1.username,"test")
        self.assertEqual(self.u2.username,"test2")

