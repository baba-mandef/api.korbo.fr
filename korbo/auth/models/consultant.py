from django.conf import settings
from django.db import models

from .token import Token

class ConsultantToken(Token):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="consultant_token_set",
        on_delete=models.CASCADE
    )
    class Meta:
        managed = True
