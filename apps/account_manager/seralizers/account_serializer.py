from rest_framework import serializers

from apps.account_manager.models import Account
from apps.account_manager.seralizers.bank_serializer import BankSerializer
from apps.core.serializers.user_simple_serializer import UserSimpleSerializer


class AccountSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    user = UserSimpleSerializer()

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "agency",
            "number",
            "type",
            "user",
            "bank",
        ]


class AccountSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "agency",
            "number",
            "type",
        ]
