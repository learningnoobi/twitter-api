from rest_framework import serializers
from .models import Message, PrivateChat
from users.serializers import UserLessInfoSerializer


class PrivateRoomSerializer(serializers.ModelSerializer):
    user1 = UserLessInfoSerializer(read_only=True)
    user2 = UserLessInfoSerializer(read_only=True)
    latest_msg = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PrivateChat
        fields = ("id", "user1", "user2","latest_msg")
    
    def get_latest_msg(self,obj):
        msg = obj.last_msg()
        serializer =  MessageSerializer(msg)
        return serializer.data




class MessageSerializer(serializers.ModelSerializer):
    sender = UserLessInfoSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ("id", "sender", "text", "created_at")
