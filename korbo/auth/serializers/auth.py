from importlib import import_module

from rest_framework import serializers

from korbo.extra.enum import TokenTypeEnum


class AuthSerializer(serializers.Serializer):
    account = serializers.SerializerMethodField(read_only=True, source="get_account")
    token = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def get_account(self, obj) -> dict:
        account_type = obj.account_type

        if account_type == TokenTypeEnum.super_user.value:
            from korbo.user.serializers import UserSerializer

            return UserSerializer(self.instance.account).data

        serializer_name = f"{account_type.capitalize()}Serializer"
        try:
            module = import_module(f"korbo.account.{account_type}.serializers")
            serializer = getattr(module, serializer_name)
        except ImportError:
            raise NotImplementedError
        return serializer(getattr(self.instance.account, account_type), context=self.context).data
