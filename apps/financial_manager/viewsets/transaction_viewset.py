from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.financial_manager.models import Transaction
from apps.financial_manager.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated,
    ]
