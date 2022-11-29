from django.contrib import admin

from .models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'id', 'last_name',
                    'first_name', 'is_staff', 'is_superuser')
