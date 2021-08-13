from django.contrib import admin
from .models import Comment, Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display=['id','title','is_parent','author']
    list_filter=['title','author']

@admin.register(Comment)
class TweetAdmin(admin.ModelAdmin):
    list_display=['body','id','post','author']