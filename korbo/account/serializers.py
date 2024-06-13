from django.utils.timezone import now

from korbo.user.serializers import UserSerializer


class AccountSerializer(UserSerializer):
    def create(self, validated_data):
        validated_data.setdefault("is_active", True)
        validated_data.setdefault("activated", now())
        return super().create(validated_data)

    class Meta:
        model = None
        fields = UserSerializer.Meta.fields + (
            'deactivate_reason',
            'last_refresh',
            'deactivated',
            'activated',
            'avatar',
            'avg_rating',
            'location',
            'number_of_reviews',
            'website',
        )
        extra_kwargs = UserSerializer.Meta.extra_kwargs | {
            'deactivate_reason': {'read_only': True},
            'last_refresh': {'read_only': True},
            'activated': {'read_only': True},
            'deactivated': {'read_only': True},
            'deactivated': {'read_only': True},
        }
     
