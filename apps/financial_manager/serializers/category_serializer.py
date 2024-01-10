from rest_framework import serializers

from apps.core.serializers.user_simple_serializer import UserSimpleSerializer
from apps.financial_manager.models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Category
        fields = [
            "id",
            "user",
            "name",
            "description",
        ]


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
        ]
