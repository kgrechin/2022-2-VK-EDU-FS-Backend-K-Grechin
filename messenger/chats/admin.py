from django.contrib import admin

from .models import Chat


@admin.register(Chat)
class AmdinChat(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_private', 'created_at', 'admin')
