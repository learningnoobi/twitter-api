from rest_framework import exceptions, serializers
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        if len(request.data['password']) < 6:
            raise exceptions.ValidationError({'error':'Passwords must be larger than 6 letters !'})

        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError({'error':'Passwords do not match  !'})

        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)