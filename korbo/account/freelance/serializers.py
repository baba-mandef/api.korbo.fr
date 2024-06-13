from korbo.account.freelance.models import Freelance
from korbo.account.serializers import AccountSerializer


class FreelanceSerializer(AccountSerializer):

    def create(self, validated_data):
        validated_data["is_password"] = True
        instance = super().create(validated_data)
      
        return instance

    class Meta:
        model = Freelance
        fields = AccountSerializer.Meta.fields + (
            "born_at",
            "phone",
            "adress",
            "is_password"
           
        )
        extra_kwargs = AccountSerializer.Meta.extra_kwargs | {"is_password": {'read_only': True}}
        
