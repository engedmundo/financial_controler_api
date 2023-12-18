from rest_framework.routers import DefaultRouter

from apps.financial_manager.viewsets import (
    BudgetViewSet,
    CategoryViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = router.urls
