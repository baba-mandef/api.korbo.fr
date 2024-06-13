from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotFound


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username:
            msg = _('Must include "username".')
            raise serializers.ValidationError({"detail": msg}, code="authorization")

        if not password:
            msg = _('Must include "password".')
            raise serializers.ValidationError({"detail": msg}, code="authorization")

        user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
        print(user)

        if not user:
            msg = _("Invalid username / password.")
            raise serializers.ValidationError({"detail": msg}, code="authorization")

        if self.context["token_type"] != "superuser":
            user = getattr(user, self.context["token_type"], None)

        if not user:
            msg = _('No %(token_type)s account found for user.') % {'token_type': self.context["token_type"]}
            raise NotFound(msg, code="authorization")

        attrs["user"] = user
        return attrs
