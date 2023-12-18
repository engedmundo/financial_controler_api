from rest_framework import viewsets

from apps.account_manager.models import Bank
from apps.account_manager.seralizers import BankSerializer
from rest_framework.permissions import IsAuthenticated


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [
        IsAuthenticated,
    ]
