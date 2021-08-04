from django.contrib import admin
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display=['id','title','is_parent','author']
    list_filter=['title','author']