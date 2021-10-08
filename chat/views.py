from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import PrivateChat
from users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def create_private_chat_room(request,username):
    user2 = User.objects.get(username=username)
    user1 = request.user
    if user1 == user2:
        print("Cannot form thread with oneself !")
    private_room = PrivateChat.objects.get_or_create(user1=user1,user2=user2)
    return Response({
        "response":"Created PrivateRoom",
        "room_id":private_room.id
    })

    