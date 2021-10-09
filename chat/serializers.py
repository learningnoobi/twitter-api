from rest_framework import serializers
from .models import Message
from users.serializers import UserLessInfoSerializer
from tweets.serializers import AnonTweetSerializer,LessCommentSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserLessInfoSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ("id","sender","text","created_at")
    
