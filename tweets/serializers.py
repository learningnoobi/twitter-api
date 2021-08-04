from rest_framework import serializers
from .models import Tweet
from users.serializers import UserSerializer
from users.models import User
class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Tweet
        fields = ['id','title','body','author','is_private','image']

    def validate(self, data):
        if len(data.get("title")) <= 0:
            raise serializers.ValidationError({'error':'title should not be blank'})
        return data
