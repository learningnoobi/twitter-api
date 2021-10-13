from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserEditSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsUserOrReadOnly
from mainproject.pagination import CustomPagination

from notifications.models import Notification


class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

# djoser


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    permission_classes = [IsUserOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


@api_view(['POST'])
def follow_unfollow(request):
    username = request.data.get('username')
    myprofile = request.user
    obj = User.objects.get(username=username)

    if obj in myprofile.following.all():
        myprofile.following.remove(obj)
        return Response({'follow': False,
                         'followers': obj.followed.count(),
                         'username': username,
                         'state':'Follow'
                         })
    else:
        myprofile.following.add(obj)
        Notification.objects.get_or_create(
            notification_type='F',
            to_user=obj,
            from_user=request.user
        )
        return Response({'follow': True,
         'followers': obj.followed.count(),
         'state':'UnFollow'}
         )

@api_view(['GET'])
def recommend_user(request):
    users = User.objects.exclude(username=request.user.username)
    users = users.exclude(id__in = request.user.following.all())[:5]
    serializer = UserSerializer(users,many=True,context={'request':request})
    return Response(serializer.data)


@api_view(['GET'])
def follow_user_list(request):
    users = User.objects.exclude(username=request.user.username)
    users = users.exclude(id__in = request.user.following.all())

    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(users,request)
    serializer = UserSerializer(result_page,many=True,context={'request':request})
    return paginator.get_paginated_response(serializer.data)