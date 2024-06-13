from rest_framework import serializers

from .auth import AuthSerializer
from .login import LoginSerializer
from .password import SetPasswordSerializer


class LogoutSerializer(serializers.Serializer):
    detail = serializers.BooleanField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    token = serializers.CharField()