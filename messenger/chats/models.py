import uuid

from django.db import models

from application.settings import AUTH_USER_MODEL


class Chat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    avatar = models.ImageField(
        null=True,
        blank=True
    )
    title = models.TextField(
        null=True,
        blank=True
    )
    is_private = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    admin = models.ForeignKey(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='admin'
    )
    members = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='chats'
    )

    def __str__(self) -> str:
        return f'{self.id}'

    class Meta:
        ordering = ['-created_at']
