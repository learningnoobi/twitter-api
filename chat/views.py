from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import PrivateChat,Message
from users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .serializers import MessageSerializer,PrivateRoomSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def create_private_chat_room(request,username):
    print('username is ',username)
    u2 = User.objects.get(username=username)
    u1 = request.user
    room =  PrivateChat.objects.filter(Q(user1=u1 ,user2=u2)| Q(user1=u2,user2=u1)).first()
    messages = Message.objects.by_room(room)
    serializer = MessageSerializer(messages,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_rooms(request):
    u1 = request.user
    rooms =  PrivateChat.objects.filter(Q(user1=u1)| Q(user2=u1))
    serializer = PrivateRoomSerializer(rooms , many=True)
    return Response(serializer.data)