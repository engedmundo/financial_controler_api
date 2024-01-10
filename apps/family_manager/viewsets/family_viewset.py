from rest_framework import viewsets

from apps.family_manager.models import Family
from apps.family_manager.serializers import FamilySerializer
from rest_framework.permissions import IsAuthenticated


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [
        IsAuthenticated,
    ]
