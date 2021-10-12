from django.http import response
from tweets.models import Tweet, Comment
from users.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from rest_framework import status
import json
from notifications.models import Notification

class TestTweetView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.u1 = User.objects.create_user(
            email="test@gmail.com", username="test", password="test123"
        )
        self.u2 = User.objects.create_user(
            email="test2@gmail.com", username="test2", password="test123"
        )
        self.tweet1 = Tweet.objects.create(
            title="first Tweet",
            author=self.u1,
        )
        self.tweet2 = Tweet.objects.create(
            title="Second tweet",
            author=self.u1,
        )
        self.response = self.client.get("/tweets/", format="json")
        self.assertEqual(self.tweet1.title, "first Tweet")

    def test_tweet_list(self):
        self.client.force_authenticate(user=self.u1)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data["data"]), 2)

    def test_tweet_meta(self):
        self.assertEqual(self.response.data["meta"]["next"], None)

    def test_add_tweet(self):
        self.client.force_authenticate(user=self.u1)
        data = {"title": "adding from here"}
        res = self.client.post(
            "/tweets/", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/tweets/", format="json")
        self.assertEqual(len(response.data["data"]), 3)

    def test_add_without_authenticated_user(self):
        data = {"title": "adding from here"}
        res = self.client.post(
            "/tweets/", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_tweet(self):
        self.client.force_authenticate(user=self.u1)
        data = {"title": "this is updated i guess"}
        response = self.client.put(
            "/tweets/1/", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tweet(self):
        self.client.force_authenticate(user=self.u1)
        response = self.client.delete("/tweets/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get("/tweets/", format="json")
        self.assertEqual(len(response.data["data"]), 1)

    def test_bookmark_list(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("bookmark-list")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bookmark_tweet(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("bookmark")
        response = self.client.post(url, {"pk": 1})
        self.assertEqual(response.data, {"bookmarked": True})
        response = self.client.post(url, {"pk": 1})
        self.assertEqual(response.data, {"bookmarked": False})

    def test_user_tweet(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("user-tweet", kwargs={"username": "test"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_explore_tweet(self):
        self.client.force_authenticate(user=self.u1)
        response = self.client.get('/tweets/explore/global/',format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LikeUnlikeTest(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com", username="test", password="test123"
        )
        self.u2 = User.objects.create_user(
            email="test2@gmail.com", username="dummy", password="test123"
        )
        self.tweet2 = Tweet.objects.create(
            title="Second tweet",
            author=self.u1,
        )
        self.tweet2 = Tweet.objects.create(
            title="third tweet",
            author=self.u2,
        )


    def test_like(self):
        self.client.force_authenticate(user=self.u1)
        response = self.client.post(reverse("like-unlike"), {"pk": 1})
        self.assertEqual(response.data, {"liked": True, "count": 1})
        unlike_res = self.client.post(reverse("like-unlike"), {"pk": 1})
        self.assertEqual(unlike_res.data, {"liked": False, "count": 0})

    def test_like_unlike_notification(self):
        self.client.force_authenticate(user=self.u1)
        self.client.post(reverse("like-unlike"), {"pk": 2})
        notifications_count = Notification.objects.count()
        self.assertEqual(notifications_count, 1)


class CommentViewTest(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com", username="test", password="test123"
        )
        self.u2 = User.objects.create_user(
            email="test2@gmail.com", username="dummy", password="test123"
        )
        self.tweet2 = Tweet.objects.create(
            title="Second tweet",
            author=self.u1,
        )
        self.tweet3 = Tweet.objects.create(
            title="dummy tweet",
            author=self.u2,
        )
        self.comment = Comment.objects.create(
            body="first", author=self.u1, post=self.tweet2
        )
        self.comment2 = Comment.objects.create(
            body="secondt", author=self.u2, post=self.tweet2
        )
        self.client.force_authenticate(user=self.u1)

    def test_get_tweet(self):
        url = reverse("comment-view", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_comment(self):
        url = reverse("comment-view", kwargs={"pk": 1})
        data = {"body": "comment"}
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        blank = {"body": ""}
        response = self.client.post(
            url, data=json.dumps(blank), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_new_comment_notification(self):
        url = reverse("comment-view", kwargs={"pk": 2})
        data = {"body": "comment"}
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        notifications_count = Notification.objects.count()
        self.assertEqual(notifications_count, 1)

    def test_reply_comment(self):
        url = reverse("comment-reply", kwargs={"pk": 1})
        data = {"comId": 1, "body": "this is reply to comment"}

        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blank_data = {"comId": 1, "body": ""}
        response = self.client.post(
            url, data=json.dumps(blank_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_reply_comment_notification(self):
        url = reverse("comment-reply", kwargs={"pk": 1})
        data = {"comId": 2, "body": "this is reply to comment"}
        self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        notifications_count = Notification.objects.count()
        self.assertEqual(notifications_count, 1)

    def test_like_unlike_comment(self):
        response = self.client.post(reverse("like-unlike-comment"), {"pk": 1})
        self.assertEqual(response.data, {"liked": True, "count": 1})
        response = self.client.post(reverse("like-unlike-comment"), {"pk": 1})
        self.assertEqual(response.data, {"liked": False, "count": 0})


class RetweetTest(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com", username="test", password="test123"
        )
        self.u2 = User.objects.create_user(
            email="test2@gmail.com", username="testing", password="test123"
        )
        self.tweet1 = Tweet.objects.create(
            title="first Tweet",
            author=self.u1,
        )
        self.tweet2 = Tweet.objects.create(
            title="second Tweet",
            author=self.u2,
        )
        print(self.tweet2.id)
        self.url = reverse("retweet-view")
        self.client.force_authenticate(user=self.u1)

    def test_retweet_view(self):
        
        
        response = self.client.post(self.url, {"tweetId": 1})
        self.assertEqual(response.data, {"detail": "Can't Retweet your own post"})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_retweet_not_found(self):
        res = self.client.post(self.url, {"tweetId": 62})
        # self.assertEqual(res.data, {"retweet": True})
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_retweet_found(self):
        res = self.client.post(self.url, {"tweetId": 2})
        self.assertEqual(res.data, {"retweet": True})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(self.url, {"tweetId": 2})
        self.assertEqual(res.data,{ "detail": "Already retweeted !"})
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


