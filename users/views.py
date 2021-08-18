from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer,UserEditSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from .permissions import IsUserOrReadOnly

class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg ='username'
    lookup_field='username'
    permission_classes = [IsUserOrReadOnly]

    def get_serializer_class(self):
        if self.request.method=="GET":
            return UserSerializer
        if self.request.method in ["PUT","DELETE"]:
            return UserEditSerializer

    