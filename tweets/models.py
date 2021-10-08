from users.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class TweetManager(models.Manager):
    # show only public field (private=False) to other user but not for the author of the tweet
    def only_public_or_author(self, user):
        if user.is_authenticated:
            user_i_follow = user.following.all()
            #showing only the posts of user i follow
            feed_tweets = Tweet.objects.filter(is_private=False,author_id__in=user_i_follow) 
            tweets = Tweet.objects.filter(author=user)
            return feed_tweets | tweets
        return Tweet.objects.filter(is_private=False)




class Tweet(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    liked = models.ManyToManyField(User, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='tweetspic')
    bookmark = models.ManyToManyField(
        User, related_name="bookmark", blank=True, default=None)
    author = models.ForeignKey(
        User, related_name="users", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name='parenttweet', null=True, blank=True)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    is_private = models.BooleanField(default=False, blank=True, null=True)
    isEdited = models.BooleanField(default=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = TweetManager()

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

    @property
    def like_count(self):
        return self.liked.count()


class Comment(models.Model):
    body = models.TextField()
    liked = models.ManyToManyField(
        User, blank=True, related_name="comment_likes")
    author = models.ForeignKey(
        User, related_name="authors", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Tweet, related_name="parent_tweet", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    isEdited = models.BooleanField(default=False, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='parentchild')

    def __str__(self):
        return str(self.body[:15])

    @property
    def is_parent(self):
        return True if self.parent is None else False

    @property
    def like_comment(self):
        return self.liked.count()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()
