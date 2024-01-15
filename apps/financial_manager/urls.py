from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.financial_manager.viewsets import (
    BudgetViewSet,
    CategoryViewSet,
    TransactionCSVViewSet,
    TransactionViewSet,
    TransactionByFamilyViewSet,
)

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("transactions/", TransactionViewSet.as_view(), name="transactions"),
    path("transactions/csv/", TransactionCSVViewSet.as_view(), name="transactions-csv"),
    path(
        "transactions/family/<int:family_id>/",
        TransactionByFamilyViewSet.as_view(),
        name="transactions-family",
    ),
]

urlpatterns += router.urls
