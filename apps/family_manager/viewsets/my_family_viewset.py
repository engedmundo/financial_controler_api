from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.family_manager.models import Family
from apps.family_manager.serializers import FamilySerializer


class MyFamilyViewSet(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = request.user
        family = Family.objects.get(members=user)
        serializer = FamilySerializer(family)
        return Response(serializer.data, status=status.HTTP_200_OK)
