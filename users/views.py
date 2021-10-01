from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer,UserEditSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from .permissions import IsUserOrReadOnly


from notifications.models import Notification
class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context  

#djoser

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    lookup_url_kwarg ='username'
    lookup_field='username'
    permission_classes = [IsUserOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context  

    # def get_serializer_class(self):
    #     if self.request.method=="GET":
    #         return UserSerializer(context={'request': self.request})
    #     if self.request.method in ["PUT","DELETE"]:
    #         return UserEditSerializer(context={'request': self.request})

@api_view(['POST'])
def follow_unfollow(request):
    username = request.data.get('username')
    myprofile = request.user
    obj = User.objects.get(username=username)
  
    if obj in myprofile.following.all():
        myprofile.following.remove(obj)
        return Response({'follow':False,
                    'followers':obj.followed.count(),
                    'username':username
        })
    else:
        myprofile.following.add(obj)
        Notification.objects.get_or_create(
            notification_type='F',
            to_user=obj,
            from_user=request.user
            )
        return Response({'follow':True,'followers':obj.followed.count()})