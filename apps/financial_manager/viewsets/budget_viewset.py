from rest_framework import viewsets

from apps.financial_manager.models import Budget
from apps.financial_manager.serializers import BudgetSerializer
from rest_framework.permissions import IsAuthenticated


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [
        IsAuthenticated,
    ]
