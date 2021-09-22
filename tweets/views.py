from rest_framework import viewsets,exceptions,status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from .models import Tweet,Comment
from .serializers import (TweetSerializer
                    ,CommentSerializer,
                    UserTweetSerializer,AnonTweetSerializer
                    )
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import generics
from users.models import User
from django.db.models import Q

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]


    def get_queryset(self):
        return Tweet.objects.only_public_or_author(self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def ReTweetView(request):
    data = request.data
    tweetId = data["tweetId"]
    try:
        tweet = Tweet.objects.get(id=tweetId)
    except:
        raise exceptions.APIException("Not Found ! ")
    if tweet.author == request.user:
        raise exceptions.APIException("Can't Retweet your own post")
    # try:
    parent_tweet = Tweet.objects.filter(parent=tweet,author=request.user)
    if parent_tweet.exists():
        raise exceptions.APIException("Already retweeted !")
    else:
        re_tweet = Tweet.objects.create(
            author=request.user,
            parent=tweet
            )
    serializer = TweetSerializer(re_tweet ,{'request':request})
    return Response({"retweet":True})
    # except Exception as e:
    #     return Response({'error':f'{e}'},status=status.HTTP_403_FORBIDDEN)




@api_view(['GET','POST','DELETE'])
@permission_classes((IsAuthenticated,))
def ComentView(request,pk):
    data = request.data
    if request.method=='GET':
        tweet = Tweet.objects.get(id=pk)
        comments = Comment.objects.filter(post=tweet,parent=None).order_by('-created')
        serializer = CommentSerializer(comments ,many=True,context={'request': request})
        return Response(serializer.data)

    if request.method=='POST':
        tweet = Tweet.objects.get(id=pk)
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        new_comment = Comment(body=data.get('body'),author=request.user,post=tweet)
        new_comment.save()
        serializer = CommentSerializer(new_comment,context={'request': request})
        return Response(serializer.data)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['POST','DELETE'])
@permission_classes((IsAuthenticated,))
def ComentReplyView(request,pk):
    data = request.data
    if request.method=='POST':
        tweet = Tweet.objects.get(id=pk)
        parentComId = data.get('comId')
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        parent = Comment.objects.get(id=parentComId)
        new_comment = Comment(parent=parent,body=data.get('body'),author=request.user,post=tweet)
        new_comment.save()
        serializer = CommentSerializer(new_comment,context={'request': request})
        return Response(serializer.data)

# @api_view(['GET'])
# def get_child(request,pk):
    
#     if request.method=='GET':
#         parent_comment = Comment.objects.get(id=pk)
#         children = parent_comment.children
#         serializer = CommentSerializer(children,many=True)
#         return Response(serializer.data)
       

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
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
    return Response({"love":"no"})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like_unlike_comment(request):
    if request.method =="POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment,id=pk)
        if request.user in comment.liked.all():
            liked = False
            comment.liked.remove(request.user)
        else:
            liked = True
            comment.liked.add(request.user)
        return Response({
            'liked':liked,
            'count':comment.like_comment
        })
    return Response({"love":"no"})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def bookmark_tweet(request):
    if request.method =="POST":
        pk = request.data.get("pk")
        tweet = get_object_or_404(Tweet,id=pk)
        if request.user in tweet.bookmark.all():
            bookmarked = False
            tweet.bookmark.remove(request.user)
        else:
            bookmarked = True
            tweet.bookmark.add(request.user)
        return Response({
            'bookmarked':bookmarked,
        })
    return Response({"bookmar":"lol"})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def UserTweetList(request,username):
    user = User.objects.get(username=username)
    if request.method=='GET':
        tweets = Tweet.objects.filter(author=user).filter(is_private=False).order_by('-created')
        if user ==request.user:
            owner_private = Tweet.objects.filter(author=request.user).filter(is_private=True)
            tweets = tweets|owner_private
        serializer = TweetSerializer(tweets, many=True,context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def bookmarkList(request):
    bookmark_tweet = request.user.bookmark.all()
    serializer = TweetSerializer(bookmark_tweet, many=True,context={'request': request})
    return Response(serializer.data)
