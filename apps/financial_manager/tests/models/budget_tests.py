import pytest

from apps.core.tests.base_test import BaseModelsTest
from apps.financial_manager.models import Budget
from apps.financial_manager.tests.factories import (
    BudgetFactory,
    CategoryFactory,
)


class BudgetModelTests(BaseModelsTest):
    def test_create_budget_model_instance(self):
        # Given
        expected_attrs = [
            "user",
            "category",
            "amount",
            "month",
            "year",
            "type",
            "description",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        category = CategoryFactory()
        budget = BudgetFactory(user=category.user, category=category)
        db_budgets = Budget.objects.all()
        db_budget = db_budgets.first()

        # Then
        self.assertIsInstance(budget, Budget)
        self.assertEqual(len(db_budgets), 1)
        self.assertEqual(str(db_budget), budget.description)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(budget, attr_name)
                budget_attr = getattr(budget, attr_name)
                db_budget_attr = getattr(db_budget, attr_name)
                self.assertEqual(budget_attr, db_budget_attr)

    def test_budget_model_meta_verbose_names(self):
        # Then
        self.assertEqual(Budget._meta.verbose_name, "Orçamento")
        self.assertEqual(Budget._meta.verbose_name_plural, "Orçamentos")


@pytest.mark.parametrize(
    "attr_name",
    ["user", "category", "amount", "month", "year", "type", "description"],
)
def test_create_budgets_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with BudgetModelTests().assertRaises(Exception):
        Budget.objects.create(**test_data)
