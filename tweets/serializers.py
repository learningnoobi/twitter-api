from rest_framework import serializers
from .models import Comment, Tweet
from users.serializers import UserSerializer
from users.models import User
from rest_framework.response import Response

from users.serializers import UserLessInfoSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    iliked = serializers.SerializerMethodField(read_only=True)
    is_parent = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)
    parentId= serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    


    class Meta:
        model = Comment
        fields = [
            'id','body','author',
            'isEdited','children','is_parent',
            'parentId','created','iliked','like_count',
            ]
    def get_iliked(self,obj):
        return True if self.context.get('request').user in obj.liked.all() else False
        
    def get_is_parent(self,obj):
        return obj.is_parent

    

    def get_parentId(self,obj):
        if obj.parent:
            return obj.parent.id
        return None

    def get_children(self,obj):
        serializer = CommentSerializer(obj.children, many=True,
        context={'request':self.context.get('request')})
        return serializer.data
    
    def get_like_count(self,obj):
        return obj.liked.count()

class UserTweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    like_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = '__all__'

    def get_like_count(self,obj):
        return obj.liked.count()  

class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    iliked = serializers.SerializerMethodField(read_only=True)
    i_bookmarked = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    myparent = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_myparent(self,obj):
        serializer = TweetSerializer(obj.parent,
        context={'request':self.context.get('request')})
        return serializer.data

    def get_iliked(self,obj):
        print('user liked :', obj.liked.all())
        print('me is ',self.context.get('request').user)
        return True if self.context.get('request').user in obj.liked.all() else False
    
    def get_i_bookmarked(self,obj):
        return True if self.context.get('request').user in obj.bookmark.all() else False

    def get_like_count(self,obj):
        return obj.liked.count()
    def get_comment_count(self,obj):
        return obj.parent_tweet.count()



class AnonTweetSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id','title','author']

class LessCommentSerializer(serializers.ModelSerializer):
    tweet_id =  serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = [ 'id','body','tweet_id']
    
    def get_tweet_id(self,obj):
        return obj.post.id