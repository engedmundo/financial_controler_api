from rest_framework import viewsets

from apps.financial_manager.models import Budget
from apps.financial_manager.serializers import BudgetSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer