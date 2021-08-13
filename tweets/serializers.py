from rest_framework import serializers
from .models import Comment, Tweet
from users.serializers import UserSerializer
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Comment
        fields = ['id','body','author','isEdited','created']
        
class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    iliked = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = '__all__'

    def get_iliked(self,obj):
        return True if self.context['request'].user in obj.liked.all() else False

    def get_like_count(self,obj):
        return obj.liked.all().count()
