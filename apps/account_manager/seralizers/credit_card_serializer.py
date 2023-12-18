from rest_framework import serializers

from apps.account_manager.models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = "__all__"
