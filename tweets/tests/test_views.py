from django.http import response
from tweets.models import Tweet
from users.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import force_authenticate
from tweets.serializers import TweetSerializer
from rest_framework.test import APIRequestFactory

import json
class TestTweetView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.u1 = User.objects.create_user(
            email="test@gmail.com", username="test", password="test123"
        )
        self.tweet1 = Tweet.objects.create(
            title="first Twet",
            author=self.u1,
        )
        self.tweet2 = Tweet.objects.create(
            title="Second tweet",
            author=self.u1,
        )
        self.response = self.client.get("/tweets/", format="json")


    def test_tweet_list(self):
        
        self.client.force_authenticate(user=self.u1)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["data"]), 2)

    def test_tweet_meta(self):
        self.assertEqual(self.response.data["meta"]["next"],None)
    
    def test_add_tweet(self):
        self.client.force_authenticate(user=self.u1)
        data= {
            "title":"adding from here"
        }
        res = self.client.post("/tweets/", data=json.dumps(data),
            content_type='application/json')
       
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        response = self.client.get("/tweets/", format="json")
        self.assertEqual(len(response.data["data"]), 3)
    
    def test_add_without_authenticated_user(self):
        data= {
            "title":"adding from here"
        }
        res = self.client.post("/tweets/", data=json.dumps(data),
            content_type='application/json')
        print('not authorized are you ?')
        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)


