from django.urls import path
from .import views
from .views import create_private_chat_room,check

urlpatterns = [
    path('create/<username>/',create_private_chat_room),
    path('check/' ,check)
]
