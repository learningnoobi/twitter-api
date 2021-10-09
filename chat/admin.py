from django.contrib import admin
from .models import PrivateChat,Message


class MessageInline(admin.StackedInline):
    model = Message
    fields = ('sender', 'text')
    readonly_fields = ('sender', 'text')

class PrivateChatAdmin(admin.ModelAdmin):
    model = PrivateChat
    inlines = (MessageInline,)
admin.site.register(PrivateChat,PrivateChatAdmin)