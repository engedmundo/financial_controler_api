from rest_framework import viewsets

from apps.account_manager.models import Bank
from apps.account_manager.seralizers import BankSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer