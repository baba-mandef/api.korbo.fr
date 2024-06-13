from rest_framework import serializers
from korbo.user.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="get_user_role", read_only=True)

    # todo; remove
    # temporary hack to fix email = ''
    def validate_email(self, value):
        if not value:
            value = None
        return value

    def create(self, validated_data):
        token_type = self.context.get("token_type")
        if token_type:
            validated_data[f"is_{token_type}"] = True
        password = validated_data.pop("password", None)
        email = validated_data.pop("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.Meta.model.objects.create_user(email, password, **validated_data)

        instance = getattr(user, token_type, None)

        if instance is None:
            validated_data.pop("first_name")
            validated_data.pop("last_name")
            instance = self.Meta.model(user_id=user.pk)
            instance.__dict__.update(user.__dict__)
            instance.__dict__.update(validated_data)
            instance.save()

        return instance

    def validate_password(self, value):
        # validate_password(value, user=self.instance)
        return value

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
            instance.is_password = True
        instance.save()

        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        if not repr_.get("email"):
            repr_["email"] = ""

        return repr_

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "sex",
            "email",
            "password",
            "created",
            "updated",
            "is_active",
        
        )
        extra_kwargs = {
            "password": {"required": True, "write_only": True},
            "last_name": {"required": True},
            "first_name": {"required": True},
            "is_active": {
                "read_only": True,
            },
        }


