from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"", views.TweetViewSet, basename="tweetslist")
router.register(r"explore/global", views.ExploreTweetViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("post/retweet/", views.ReTweetView , name="retweet-view"),
    path("comments/<int:pk>/", views.ComentView.as_view(), name="comment-view"),
    path(
        "comment_detail/<int:pk>/",
        views.CommentDetail.as_view(),
        name="comment-create-list",
    ),
    path("comments/reply/<int:pk>/", views.ComentReplyView, name="comment-reply"),
    path("love/like-unlike/", views.like_unlike_tweet, name="like-unlike"),
    path(
        "love/like-unlike-comment/",
        views.like_unlike_comment,
        name="like-unlike-comment",
    ),
    path("love/bookmark/", views.bookmark_tweet, name="bookmark"),
    path("love/bookmarkList/", views.bookmarkList, name="bookmark-list"),
    path("search/custom/", views.SearchList.as_view()),
    path("specific/<username>/", views.UserTweetList,name="user-tweet"),
]
