from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from korbo.extra.tools import generate_token, check_key, validate_jwt
from korbo.extra.enum import TokenTypeEnum
from django.conf import settings



class RefreshTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    msg = "Invalid username or password."
    token_type = None
    _request = None
    _user = None
    _user_model = get_user_model()

    def authenticate_header(self, request):
        return self.keyword

    def authenticate(self, request):
        self._request = request

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(self.msg)

        if len(auth) == 1 or len(auth) > 2:
            raise exceptions.AuthenticationFailed(self.msg)

        try:
            token_jwt = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed(self.msg)
        return self.authenticate_credentials(token_jwt)

    def authenticate_credentials(self, token_jwt):
        payload = validate_jwt(token_jwt)
        try:
            self.token_type = payload['role']
            user = self._user_model.objects.get_by_public(payload["id"])
        except (ObjectDoesNotExist, KeyError):
            return None
        
        if self.token_type != TokenTypeEnum.super_user.value:

            try:
                self._user = getattr(user, self.token_type)
            except AttributeError:
                return None
            
            user = self._user
        
        if not user.has_role(self.token_type) or not user.is_active:
            return None
        
        try:
            token = getattr(user, f"{self.token_type}_token_set").get(public_id=payload["token"])

        except (self.model.DoesNotExist, AttributeError, KeyError):
            return None
        
        key = token.refresh

        if not check_key(key, payload["key"]):
            return None
        
        return user, self.token_type
    
 