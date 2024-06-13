from korbo.auth.models import ConsultantToken
from .base import BaseJWTAuth


class ConsultantJWTAuthentication(BaseJWTAuth):
    model = ConsultantToken
    token_type = "consultant"
