from django.test import TestCase
from tweets.models import Tweet, Comment
from users.models import User
# Create your tests here.
import logging

class TestTweetModel(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com",
            username="test", password="test123")
        self.tweet1 = Tweet.objects.create(
            title="first Twet",
            author=self.u1
        )
        self.tweet2 = Tweet.objects.create(
            title="first Twet",
            author=self.u1,
            parent=self.tweet1
        )

    def test_tweet_has_parent(self):
        self.assertTrue(self.tweet1.is_parent)
        self.assertFalse(self.tweet2.is_parent)
    
    def test_like_count(self):
        self.tweet1.liked.add(self.u1)
        self.assertEqual(self.tweet1.like_count,1)
        self.assertNotEqual(self.tweet1.like_count,31)
        
