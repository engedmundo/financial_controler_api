from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.financial_manager.viewsets import (
    BudgetViewSet,
    CategoryViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("transactions/", TransactionViewSet.as_view(), name="transactions"),
]

urlpatterns += router.urls
