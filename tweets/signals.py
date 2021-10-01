from django.dispatch import receiver    
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


msg = {
    "L":"liked your tweet",
    "R":"replied your tweet",
    "F":"followed you ",
}

def noti_msg(type):
    return msg[type]


@receiver(post_save,sender=Notification)
def create_notification(sender, instance, created, *args, **kwargs):
    from_user = instance.from_user.username
    to_user = instance.to_user.username
    noti_type = instance.notification_type #L
    msg = noti_msg(noti_type)
    noti_count = Notification.objects.filter(
        to_user=instance.to_user,
        user_has_seen=False
        ).count()
    print("from user " ,from_user)
    print("to user ", to_user)
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        f'love_{to_user}',
            {
                "type":"send_status",
                "from":from_user,
                "data":f"{from_user} {msg}",
                "count":noti_count
            }
        )

