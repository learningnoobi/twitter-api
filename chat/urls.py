from django.urls import path
from .import views
from .views import create_private_chat_room,get_rooms

urlpatterns = [
    path('create/<username>/',create_private_chat_room),
    path('get_rooms/' ,get_rooms)
]
