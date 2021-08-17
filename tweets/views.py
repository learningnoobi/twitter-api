from rest_framework import viewsets,exceptions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Tweet,Comment
from .serializers import TweetSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import generics

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET','POST','DELETE'])
def ComentView(request,pk):
    data = request.data
    if request.method=='GET':
        tweet = Tweet.objects.get(id=pk)
        comments = Comment.objects.filter(post=tweet).order_by('-created')
        serializer = CommentSerializer(comments ,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        tweet = Tweet.objects.get(id=pk)
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        new_comment = Comment(body=data.get('body'),author=request.user,post=tweet)
        new_comment.save()
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(['POST'])
def like_unlike_tweet(request):
    if request.method =="POST":
        pk = request.data.get("pk")
        tweet = get_object_or_404(Tweet,id=pk)
        if request.user in tweet.liked.all():
            liked = False
            tweet.liked.remove(request.user)
        else:
            liked = True
            tweet.liked.add(request.user)
        return Response({
            'liked':liked,
            'count':tweet.like_count
        })
    return Response({"love":"me"})