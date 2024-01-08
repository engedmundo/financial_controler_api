from django.db.models import Sum
from django.db.models.query import QuerySet

from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.models import Transaction


class TransactionService:
    def __init__(self, transactions: QuerySet[Transaction]) -> None:
        self.receipts = transactions.filter(type=FinancialTypeEnum.RECEIPT)
        self.expenses = transactions.filter(type=FinancialTypeEnum.EXPENSE)
        self.total_receipt = 0
        self.total_expense = 0

    def get_transactions_summary(self) -> dict:
        total_receipt = self.receipts.aggregate(result=Sum("amount"))["result"]
        self.total_receipt = total_receipt if total_receipt else 0
        receipts_by_category = self._get_receipts_by_category()

        total_expense = self.expenses.aggregate(result=Sum("amount"))["result"]
        self.total_expense = total_expense if total_expense else 0
        expenses_by_category = self._get_expenses_by_category()

        balance = self.total_receipt - self.total_expense

        return {
            "receipt": {
                "total": self.total_receipt,
                "categories": receipts_by_category,
            },
            "expense": {
                "total": self.total_expense,
                "categories": expenses_by_category,
            },
            "balance": balance,
        }

    def _get_receipts_by_category(self) -> list:
        values_qs = self.receipts.values("category__name", "amount")
        receipts_by_category_dict = dict()

        for value in values_qs:
            category = value["category__name"]
            if category not in receipts_by_category_dict:
                receipts_by_category_dict[category] = 0

            receipts_by_category_dict[category] += value["amount"]

        receipts_by_category = [
            {
                "category": category_name,
                "total": total,
                "percentual": self._calculate_percentual(total, self.total_receipt),
            }
            for category_name, total in receipts_by_category_dict.items()
        ]

        return receipts_by_category

    def _get_expenses_by_category(self) -> list:
        values_qs = self.expenses.values("category__name", "amount")
        expenses_by_category_dict = dict()

        for value in values_qs:
            category = value["category__name"]
            if category not in expenses_by_category_dict:
                expenses_by_category_dict[category] = 0

            expenses_by_category_dict[category] += value["amount"]

        expsenses_by_category = [
            {
                "category": category_name,
                "total": total,
                "percentual": self._calculate_percentual(total, self.total_expense),
            }
            for category_name, total in expenses_by_category_dict.items()
        ]

        return expsenses_by_category

    def _calculate_percentual(self, category_value, total_value):
        if total_value == 0:
            return 100

        return round(category_value / total_value * 100, 2)
