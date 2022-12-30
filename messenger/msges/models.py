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
    text = models.TextField(
        null=True,
        blank=True
    )
    voice = models.FileField(
        null=True,
        blank=True,
        upload_to='message_voices/'
    )
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


class MessageImage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='message_images/',
    )

    def __str__(self) -> str:
        return str(self.image)
