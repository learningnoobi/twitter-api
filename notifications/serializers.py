from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)
    noti_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'
    
    def get_noti_count(self,obj):
        count = self.context.get('noti_count')
        return count
