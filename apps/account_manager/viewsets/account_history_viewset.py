from rest_framework import viewsets

from apps.account_manager.models import AccountHistory
from apps.account_manager.seralizers import AccountHistorySerializer

class AccountHistoryViewSet(viewsets.ModelViewSet):
    queryset = AccountHistory.objects.all()
    serializer_class = AccountHistorySerializer