from django.db import models
from users.models import User
from tweets.models import Tweet,Comment
# Create your models here.
class Notification(models.Model):
  
    types = [
        ('L','love'),
        ('F','follow'),
        ('M','message'),
        ('R','reply'),
    ]
    notification_type = models.CharField(max_length=2,choices=types,default=None)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'from {self.from_user} to {self.to_user}'