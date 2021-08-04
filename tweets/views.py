from rest_framework import exceptions,viewsets
from rest_framework.decorators import api_view
from .models import Tweet
from .serializers import TweetSerializer
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)