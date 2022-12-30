from django.contrib import admin

from .models import Message, MessageImage


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'chat', 'is_read', 'created_at')


@admin.register(MessageImage)
class AdminMessageImage(admin.ModelAdmin):
    list_display = ('id', 'message', 'image')
