from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .import views
router = DefaultRouter()
router.register(r'', views.TweetViewSet)
urlpatterns = [
    
    path('', include(router.urls)),
    path('comments/<int:pk>/',views.ComentView),
    path('comment_detail/<int:pk>/', views.CommentDetail.as_view()),
    path('love/like-unlike/', views.like_unlike_tweet),
    path('love/bookmark/', views.bookmark_tweet),
    path('specific/<username>/',views.UserTweetList)
    
]
    