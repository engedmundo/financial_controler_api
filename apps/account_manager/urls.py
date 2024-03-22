from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.account_manager.viewsets import (
    AccountHistoryViewSet,
    AccountViewSet,
    BankViewSet,
    CreditCardViewSet,
)

router = DefaultRouter()
router.register(
    r"account-histories", AccountHistoryViewSet, basename="account-history"
)

urlpatterns = [
    path("banks/", BankViewSet.as_view(), name="banks"),
    path("accounts/", AccountViewSet.as_view(), name="accounts"),
    path("credit-cards/", CreditCardViewSet.as_view(), name="credit-cards"),
]

urlpatterns += router.urls
