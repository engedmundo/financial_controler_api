from rest_framework import serializers

from apps.account_manager.seralizers import (
    AccountSimpleSerializer,
    CreditCardSimpleSerializer,
)
from apps.core.serializers.user_simple_serializer import UserSimpleSerializer
from apps.financial_manager.models import Transaction
from apps.financial_manager.serializers import CategorySimpleSerializer


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    account = AccountSimpleSerializer()
    credit_card = CreditCardSimpleSerializer()
    category = CategorySimpleSerializer()
    date = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "account",
            "credit_card",
            "category",
            "amount",
            "date",
            "type",
            "description",
        ]
