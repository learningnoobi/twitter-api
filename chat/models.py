from django.db import models
from users.models import User
# Create your models here.


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
    
    def __str__(self) -> str:
        return f'Chat : {self.user1} - {self.user2}'
    

class Message(BaseModel):
    room = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Room - {self.room}>'