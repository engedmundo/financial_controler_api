from django.db.models import Sum
from django.db.models.query import QuerySet

from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.models import Transaction


class TransactionService:
    @staticmethod
    def get_transactions_summary(transactions: QuerySet[Transaction]) -> dict:
        receipts = transactions.filter(type=FinancialTypeEnum.RECEIPT)
        expenses = transactions.filter(type=FinancialTypeEnum.EXPENSE)
        total_receipt = receipts.aggregate(result=Sum("amount"))["result"]
        total_receipt = total_receipt if total_receipt else 0
        total_expense = expenses.aggregate(result=Sum("amount"))["result"]
        total_expense = total_expense if total_expense else 0
        balance = total_receipt - total_expense

        response = {
            "receipt": total_receipt,
            "expense": total_expense,
            "balance": balance,
        }

        return response
