from rest_framework import serializers

from apps.family_manager.models import Family


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = "__all__"