from rest_framework import viewsets

from apps.account_manager.models import CreditCard
from apps.account_manager.seralizers import CreditCardSerializer
from rest_framework.permissions import IsAuthenticated


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [
        IsAuthenticated,
    ]
