from korbo.auth.models import FreelanceToken
from .base import BaseJWTAuth


class FreelanceJWTAuthentication(BaseJWTAuth):
    model = FreelanceToken
    token_type = "freelance"
