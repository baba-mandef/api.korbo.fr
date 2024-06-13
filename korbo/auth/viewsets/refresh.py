from importlib import import_module

from django.utils.timezone import now

from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from korbo.auth.authentications import RefreshTokenAuthentication
from korbo.auth.serializers import RefreshSerializer
from korbo.extra.enum import TokenTypeEnum
from korbo.extra.tools import validate_jwt


class RefreshTokenViewSet(ViewSet):
    http_method_names = ["post"]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (RefreshTokenAuthentication,)
    serializer_class = RefreshSerializer

    def get_token(self, user):
        token_type = self.request.auth
        if token_type == TokenTypeEnum.super_user.value:
            token_type = "admin"

        try:
            module = import_module(f"korbo.auth.authentications")
            auth_class = getattr(module, f"{token_type.capitalize()}JWTAuthentication")
        except (ModuleNotFoundError, AttributeError) as e:
            from rest_framework import exceptions

            raise exceptions.NotFound()

        return auth_class().get_auth_token(self.request, user, token_id=self.get_token_id())

    def get_token_id(self):
        token_jwt = get_authorization_header(self.request).split()[1].decode()
        payload = validate_jwt(token_jwt)
        if not payload:
            raise AuthenticationFailed()
        return payload["token"]

    def create(self, request, *args, **kwargs):
        user = request.user
        user.type = request.auth

        token, refresh = self.get_token(user)
        # todo; add support for superuser, temporary fix before adding superuser table
        if hasattr(user, "last_refresh"):
            user.last_refresh = now()
            user.save(update_fields=("last_refresh",))

        return Response({"token": token, "refresh": refresh}, status=status.HTTP_200_OK)
