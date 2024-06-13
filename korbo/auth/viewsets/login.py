from collections import namedtuple
from importlib import import_module

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from korbo.auth.serializers import LoginSerializer, AuthSerializer
from korbo.extra.enum import TokenTypeEnum


class LoginViewSet(ViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    def get_token(self, user):
        token_type = self.kwargs["token_type"]
        if token_type == TokenTypeEnum.super_user.value:
            token_type = "admin"

        try:
            module = import_module(f"korbo.auth.authentications")
            auth_class = getattr(module, f"{token_type.capitalize()}JWTAuthentication")
        except (ModuleNotFoundError, AttributeError) as e:
            from rest_framework import exceptions

            raise exceptions.NotFound()

        return auth_class().get_auth_token(self.request, user, force_refresh=False)

    def create(self, request, *args, **kwargs):
        token_type = self.kwargs["token_type"]
        if token_type == "admin":
            token_type = TokenTypeEnum.super_user.value

        serializer = LoginSerializer(
            data=request.data,
            context={"request": request, "token_type": token_type},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, refresh = self.get_token(user)

        account = AuthSerializer(
            namedtuple(
                "Auth",
                ["account", "token", "refresh", "account_type"],
                defaults=[user, token, refresh, token_type],
            )(),
            context={"request": request},
        )

        return Response(account.data, status=status.HTTP_200_OK)
