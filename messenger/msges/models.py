import uuid

from django.db import models

from application.settings import AUTH_USER_MODEL
from chats.models import Chat


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_read = models.BooleanField(
        default=False
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='messages'
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ['-created_at']
