from rest_framework import serializers
from .models import Comment, Tweet
from users.serializers import UserSerializer
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Comment
        fields = ['id','body','author']
        
class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    parent_tweet = CommentSerializer(many=True,read_only=True)

    class Meta:
        model = Tweet
        fields = ['id','title','body','author','is_private','image','parent_tweet']

    def validate(self, data):
        if len(data.get("title")) <= 0:
            raise serializers.ValidationError({'error':'title should not be blank'})
        return data