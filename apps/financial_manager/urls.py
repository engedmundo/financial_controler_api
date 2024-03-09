from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.financial_manager.views import TransactionsReportView
from apps.financial_manager.viewsets import (
    BudgetViewSet,
    CategoryViewSet,
    TransactionByFamilyViewSet,
    TransactionCSVViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budget")

urlpatterns = [
    path(
        "transactions/",
        TransactionViewSet.as_view(),
        name="transactions",
    ),
    path(
        "transactions/csv/",
        TransactionCSVViewSet.as_view(),
        name="transactions-csv",
    ),
    path(
        "transactions/family/<int:family_id>/",
        TransactionByFamilyViewSet.as_view(),
        name="transactions-family",
    ),
    path(
        "categories/",
        CategoryViewSet.as_view(),
        name="categories",
    ),
    path(
        "transactions/report/",
        TransactionsReportView.as_view(),
        name="transactions-report",
    ),
]

urlpatterns += router.urls
