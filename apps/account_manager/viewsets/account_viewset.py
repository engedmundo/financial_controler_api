from rest_framework import viewsets

from apps.account_manager.models import Account
from apps.account_manager.seralizers import AccountSerializer
from rest_framework.permissions import IsAuthenticated


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [
        IsAuthenticated,
    ]
