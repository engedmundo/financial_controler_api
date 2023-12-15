from rest_framework import viewsets

from apps.financial_manager.models import Category
from apps.financial_manager.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer