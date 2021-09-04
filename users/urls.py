from django.urls import path
from .views import UsersList,UserDetailView,follow_unfollow
urlpatterns = [
    path('users/' , UsersList.as_view() ),
    path('user/me/follow_unfollow/' , follow_unfollow ),
    path('user/<username>/' , UserDetailView.as_view() )
]
