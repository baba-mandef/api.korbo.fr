from collections import namedtuple
from importlib import import_module

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from korbo.auth.serializers import AuthSerializer
from rest_framework.permissions import AllowAny


class RegisterViewSet(ViewSet):
    authentication_classes = ()
    permission_classes = (AllowAny)
    http_method_names = ["post"]

    def get_token(self, user):
        token_type = self.kwargs["token_type"]

        try:
            module = import_module(f"korbo.auth.authentications")
            auth_class = getattr(
                module, f"{token_type.capitalize()}JWTAuthentication")
        except (ModuleNotFoundError, AttributeError) as e:
            from rest_framework import exceptions

            raise exceptions.NotFound()

        return auth_class().get_auth_token(self.request, user, force_refresh=False)

    def get_serializer_class(self):
        token_type = self.kwargs["token_type"]

        serializer_name = f"{token_type.capitalize()}Serializer"
        try:
            module = import_module(f"korbo.account.{token_type}.serializers")
            serializer_class = getattr(module, serializer_name)
        except ImportError:
            raise NotImplementedError
        return serializer_class

    def create(self, *args, **kwargs):
        token_type = self.kwargs["token_type"]
        if not token_type:
            return Response({"error": "'token_type' is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer_class()(
            data=self.request.data,
            context={"request": self.request, "token_type": token_type},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.instance

        token, refresh = self.get_token(user)
        account = AuthSerializer(
            namedtuple(
                "Auth",
                ["account", "token", "refresh", "account_type"],
                defaults=[user, token, refresh, token_type],
            )(),
            context={"request": self.request},
        )

        return Response(account.data, status=status.HTTP_201_CREATED)
