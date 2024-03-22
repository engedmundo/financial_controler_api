from rest_framework import serializers

from apps.core.serializers.user_simple_serializer import UserSimpleSerializer
from apps.family_manager.models import Family


class FamilySerializer(serializers.ModelSerializer):
    members = UserSimpleSerializer(many=True)

    class Meta:
        model = Family
        fields = [
            "id",
            "name",
            "members",
        ]
