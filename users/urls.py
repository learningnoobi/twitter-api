from django.urls import path
from .views import UsersList,UserDetailView
urlpatterns = [
    path('users/' , UsersList.as_view() ),
    path('user/<username>/' , UserDetailView.as_view() )
]
