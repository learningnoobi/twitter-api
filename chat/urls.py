from django.urls import path
from .import views
from .views import (create_private_chat_room)

urlpatterns = [
    path('create-room/<str:username>/ ',create_private_chat_room),
]
