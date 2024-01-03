from rest_framework import serializers

from apps.account_manager.models import CreditCard
from apps.account_manager.seralizers.bank_serializer import BankSerializer
from apps.core.serializers.user_simple_serializer import UserSimpleSerializer


class CreditCardSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    user = UserSimpleSerializer()

    class Meta:
        model = CreditCard
        fields = [
            "id",
            "name",
            "expense_limit",
            "payment_day",
            "user",
            "bank",
        ]
