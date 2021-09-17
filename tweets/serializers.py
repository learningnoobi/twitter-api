from rest_framework import serializers
from .models import Comment, Tweet
from users.serializers import UserSerializer
from users.models import User
from rest_framework.response import Response


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    is_parent = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)
    parentId= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id','body','author','isEdited','children','is_parent','parentId','created']
    
    def get_is_parent(self,obj):
        return obj.is_parent

    def get_parentId(self,obj):
        # return self.context['parentId']
        if obj.parent:
            return obj.parent.id
        return None

    def get_children(self,obj):
        serializer = CommentSerializer(obj.children, many=True)
        return serializer.data

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
    class Meta:
        model = Tweet
        fields = '__all__'

    def get_iliked(self,obj):
        return True if self.context['request'].user in obj.liked.all() else False
    def get_i_bookmarked(self,obj):
        return True if self.context['request'].user in obj.bookmark.all() else False
    def get_like_count(self,obj):
        return obj.liked.count()

class AnonTweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    like_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = '__all__'
    def get_like_count(self,obj):
        return obj.liked.count()