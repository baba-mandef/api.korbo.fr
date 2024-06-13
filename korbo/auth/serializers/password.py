from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from korbo.account.freelance.models import Freelance




class SetPasswordSerializer(serializers.Serializer):
    account = serializers.UUIDField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        account = attrs.get("account")
        freelance = Freelance.objects.get_by_public(account, email=email)
        attrs["freelance"] = freelance

        return attrs

    def set_password(self, validated_data):
        freelance = validated_data["freelance"]

        freelance.set_password(validated_data["password"])
        freelance.is_password = True
        if validated_data.get("email"):
            freelance.email = self.validated_data["email"]

        freelance.save(update_fields=["password", "email", "updated"])
        return freelance
