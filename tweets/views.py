from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import Tweet,Comment
from .serializers import TweetSerializer,CommentSerializer
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET','POST'])
def ComentView(request,pk):
    
    if request.method=='GET':
        tweet = Tweet.objects.get(id=pk)
        comments = Comment.objects.filter(post=tweet).order_by('-created')
        serializer = CommentSerializer(comments ,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        data = request.data
        tweet = Tweet.objects.get(id=pk)
        new_comment = Comment(body=data.get('body'),author=request.user,post=tweet)
        new_comment.save()
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)
