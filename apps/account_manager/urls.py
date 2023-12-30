from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.account_manager.viewsets import (AccountHistoryViewSet,
                                           AccountViewSet, BankViewSet,
                                           CreditCardViewSet)

router = DefaultRouter()
router.register(r"account-histories", AccountHistoryViewSet, basename="account-history")
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"credit-cards", CreditCardViewSet, basename="credit-card")

urlpatterns = [
    path('banks/', BankViewSet.as_view(), name='bank-list'),
]

urlpatterns += router.urls
