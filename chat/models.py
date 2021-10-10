from django.db import models
from users.models import User
from django.db.models import Q

class MessageManager(models.Manager):
    def by_room(self, room):
        messages = Message.objects.filter(room=room).order_by("created_at")
        return messages

class PrivateChatManager(models.Manager):
    def create_room_if_none(self,u1,u2):
        has_room = PrivateChat.objects.filter(Q(user1=u1 ,user2=u2)| Q(user1=u2,user2=u1)).first()
        if not has_room:
            print('not found so creating one ')
            PrivateChat.objects.create(user1=u1,user2=u2)
        return has_room  



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PrivateChat(BaseModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    connected_users = models.ManyToManyField(
        User, blank=True, related_name="connected_users")
    is_active = models.BooleanField(default=False)
    objects = PrivateChatManager()


    def connect(self,user):
        is_added = False
        if not user in self.connected_users.all():
            self.connected_users.add(user)
            is_added = True
        return is_added
    
    def disconnect(self,user):
        is_removed = False
        if not user in self.connected_users.all():
            self.connected_users.remove(user)
            is_removed = True
        return is_removed
    
    def last_msg(self):
        return self.message_set.all().last()
    
    def __str__(self) -> str:
        return f'Chat : {self.user1} - {self.user2}'
    

class Message(BaseModel):
    room = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    objects = MessageManager()

    def __str__(self) -> str:
        return f'From <Room - {self.room}>'