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
        total_expense = self.expenses.aggregate(result=Sum("amount"))["result"]
        self.total_expense = total_expense if total_expense else 0
        balance = self.total_receipt - self.total_expense

        return {
            "receipt": self.total_receipt,
            "expense": self.total_expense,
            "balance": balance,
        }

    def get_transactions_by_category_summary(self) -> dict:
        receipts_by_category = self._get_receipts_by_category()
        expenses_by_category = self._get_expenses_by_category()
        summary_by_category = self._merge_summary_by_category_results(
            receipts=receipts_by_category,
            expenses=expenses_by_category,
        )
        return summary_by_category

    def _get_receipts_by_category(self) -> list:
        receipts_by_category_qs = (
            self.receipts.values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("amount")
        )
        receipts_by_category = [
            {
                "category": transaction["category__name"],
                "expense": 0,
                "percentual_expense": 0,
                "receipt": transaction["total"],
                "percentual_receipt": round(
                    transaction["total"] / self.total_receipt * 100, 2
                ),
            }
            for transaction in receipts_by_category_qs
        ]
        return receipts_by_category

    def _get_expenses_by_category(self) -> list:
        expenses_by_category_qs = (
            self.expenses.values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("amount")
        )
        expenses_by_category = [
            {
                "category": transaction["category__name"],
                "expense": transaction["total"],
                "percentual_expense": round(
                    transaction["total"] / self.total_expense * 100, 2
                ),
                "receipt": 0,
                "percentual_receipt": 0,
            }
            for transaction in expenses_by_category_qs
        ]
        return expenses_by_category

    def _merge_summary_by_category_results(
        self, receipts: list, expenses: list
    ) -> list:
        summaries = receipts + expenses
        summary_dict = dict()

        for item in summaries:
            category = item["category"]

            if category not in summary_dict:
                summary_dict[category] = self._create_summary_item(category)

            summary_dict[category]["expense"] += item["expense"]
            summary_dict[category]["receipt"] += item["receipt"]
            summary_dict[category]["percentual_expense"] += item["percentual_expense"]
            summary_dict[category]["percentual_receipt"] += item["percentual_receipt"]

        summary_by_category = list(summary_dict.values())
        return summary_by_category

    @staticmethod
    def _create_summary_item(category) -> dict:
        return {
            "category": category,
            "expense": 0,
            "percentual_expense": 0,
            "receipt": 0,
            "percentual_receipt": 0,
        }
