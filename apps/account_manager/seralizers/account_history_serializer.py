from rest_framework import serializers

from apps.account_manager.models import AccountHistory


class AccountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHistory
        fields = "__all__"
