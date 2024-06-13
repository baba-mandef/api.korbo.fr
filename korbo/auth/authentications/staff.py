from korbo.auth.models import StaffToken
from .base import BaseJWTAuth


class BusinessJWTAuthentication(BaseJWTAuth):
    model = StaffToken
    token_type = "staff"
