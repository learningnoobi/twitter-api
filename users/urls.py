from django.urls import path
from .views import UsersList, UserDetailView, follow_unfollow, recommend_user
urlpatterns = [
    path('users/', UsersList.as_view()),
    path('recommend_users/forme/', recommend_user),
    path('user/me/follow_unfollow/', follow_unfollow),
    path('user/<username>/', UserDetailView.as_view())
]
