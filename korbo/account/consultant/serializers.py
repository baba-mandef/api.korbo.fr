from korbo.account.consultant.models import Business
from korbo.account.serializers import AccountSerializer



class ConsultantSerializer(AccountSerializer):

    def create(self, validated_data):
        password = validated_data["password"]
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = Business
        fields = AccountSerializer.Meta.fields

