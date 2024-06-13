from django.conf import settings
from django.db import models

from .token import Token

class AdminToken(Token):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="superuser_token_set",
        on_delete=models.CASCADE
    )
    class Meta:
        managed = True
