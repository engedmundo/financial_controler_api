from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.financial_manager.models import Category
from apps.financial_manager.serializers import CategorySimpleSerializer
from rest_framework.permissions import IsAuthenticated
from apps.family_manager.models import Family


class CategoryViewSet(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = request.user
        family = Family.objects.filter(
            members=user,
        ).first()

        if family:
            categories = Category.objects.filter(
                user__in=family.members.all(),
            )

        else:
            categories = Category.objects.filter(user=user)

        serializer = CategorySimpleSerializer(categories, many=True)
        return Response(serializer.data)
