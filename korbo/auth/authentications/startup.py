from korbo.auth.models import StartupToken
from .base import BaseJWTAuth


class StartupJWTAuthentication(BaseJWTAuth):
    model = StartupToken
    token_type = "startup"
