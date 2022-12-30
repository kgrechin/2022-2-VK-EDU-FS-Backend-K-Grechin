import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='user_avatars/',
        default='default/account.png'
    )
    bio = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.username
