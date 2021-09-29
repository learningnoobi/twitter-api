from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class TweetAdmin(admin.ModelAdmin):
    list_display=['id','notification_type','to_user','from_user']
    
