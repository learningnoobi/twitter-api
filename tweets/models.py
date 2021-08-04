from users.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Tweet(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    liked = models.ManyToManyField(User, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='tweetspic')
    bookmark = models.ManyToManyField(User,related_name="bookmark",blank=True,default=None)
    author = models.ForeignKey(User, related_name="users",on_delete=models.CASCADE)
    parent =models.ForeignKey("self", on_delete=models.CASCADE, related_name='parenttweet',null=True, blank=True)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    is_private = models.BooleanField(default=False,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _("Tweet")
        verbose_name_plural = _("Tweets")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Tweet_detail", kwargs={"pk": self.pk})
    
    @property
    def is_parent(self):
        return True if self.parent is None else False
