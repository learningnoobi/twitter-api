from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import PrivateChat, Message
from users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .serializers import MessageSerializer, PrivateRoomSerializer
from mainproject.pagination import CustomPagination

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def return_chat_messages(request, username):
    print('username is ', username)
    u2 = User.objects.get(username=username)
    u1 = request.user
    room = PrivateChat.objects.filter(
        Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()
    messages = Message.objects.by_room(room)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(messages,request)

    serializer = MessageSerializer(result_page, many=True)
    # return Response(serializer.data)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET','POST'])
def get_rooms(request):
    u1 = request.user
    if request.method=="GET":
        rooms = PrivateChat.objects.filter(Q(user1=u1) | Q(user2=u1))
    if request.method=="POST":
        other_user = request.data.get("other_user", None)
        rooms = PrivateChat.objects.filter(
            Q(user1__username__icontains=other_user, user2=u1) |
            Q(user1=u1, user2__username__icontains=other_user
              ))
    serializer = PrivateRoomSerializer(rooms, many=True)
    return Response(serializer.data)

