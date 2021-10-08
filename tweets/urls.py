from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .import views
router = DefaultRouter()

router.register(r'', views.TweetViewSet)
router.register(r'explore/global',views.ExploreTweetViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # path('explore/global/', views.ExploreTweetViewSet.as_view()),
    path('post/retweet/',views.ReTweetView),
    path('comments/<int:pk>/',views.ComentView.as_view()),
    path('comment_detail/<int:pk>/', views.CommentDetail.as_view()),
    path('comments/reply/<int:pk>/',views.ComentReplyView),
    path('love/like-unlike/', views.like_unlike_tweet),
    path('love/like-unlike-comment/',views.like_unlike_comment),
    path('love/bookmark/', views.bookmark_tweet),
    path('love/bookmarkList/',views.bookmarkList),
    path('search/custom/',views.SearchList.as_view()),
    path('specific/<username>/',views.UserTweetList)
    
]
    