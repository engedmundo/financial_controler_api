from rest_framework import viewsets

from apps.family_manager.models import Family
from apps.family_manager.serializers import FamilySerializer


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer