from django.urls import path
from .views import UsersList, register
urlpatterns = [
    path('users/' , UsersList.as_view() ),
     path('register/' , register.as_view() )
]
