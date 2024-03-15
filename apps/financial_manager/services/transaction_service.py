from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.db.models.query import QuerySet

from apps.family_manager.models import Family
from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.models import Transaction, Category
from apps.account_manager.models import Account, CreditCard


class TransactionService:
    def get_transactions_queryset(
        self,
        filter_params: dict,
        user: User,
    ) -> QuerySet[Transaction]:
        start_date = filter_params["start_date"]
        end_date = filter_params["end_date"]
        display_family = filter_params["display_family"]
        display_receipt = filter_params["display_receipt"]
        display_expense = filter_params["display_expense"]

        raw_transactions = Transaction.objects.filter(
            date__gte=start_date,
            date__lte=end_date,
        )

        user_transactions = self.filter_transactions_by_family_members(
            raw_transactions,
            user,
            display_family,
        )

        transactions = self.filter_transactions_by_type(
            user_transactions,
            display_receipt,
            display_expense,
        )

        return transactions

    def filter_transactions_by_family_members(
        self,
        transactions: QuerySet[Transaction],
        user: User,
        display_family: bool,
    ) -> QuerySet[Transaction]:
        if not display_family:
            return transactions.filter(
                user=user,
            )

        family_members = self.get_family_members(user)
        return transactions.filter(
            Q(user=user) | Q(user__in=family_members),
        )

    def get_family_members(self, user: User) -> QuerySet[User]:
        family = Family.objects.filter(
            members=user,
        ).first()
        return family.members.all()

    def filter_transactions_by_type(
        self,
        transactions: QuerySet[Transaction],
        display_receipt: bool,
        display_expense: bool,
    ) -> QuerySet[Transaction]:
        if not display_receipt:
            transactions = transactions.exclude(
                type=FinancialTypeEnum.RECEIPT,
            )

        if not display_expense:
            transactions = transactions.exclude(
                type=FinancialTypeEnum.EXPENSE,
            )

        return transactions

    def get_transactions_summary(
        self, transactions: QuerySet[Transaction]
    ) -> dict:
        receipts = transactions.filter(type=FinancialTypeEnum.RECEIPT)
        total_receipt = receipts.aggregate(result=Sum("amount"))["result"]
        total_receipt = total_receipt if total_receipt else 0
        receipts_by_category = self._get_receipts_by_category(
            receipts, total_receipt
        )

        expenses = transactions.filter(type=FinancialTypeEnum.EXPENSE)
        total_expense = expenses.aggregate(result=Sum("amount"))["result"]
        total_expense = total_expense if total_expense else 0
        expenses_by_category = self._get_expenses_by_category(
            expenses, total_expense
        )

        balance = total_receipt - total_expense

        return {
            "receipt": {
                "total": total_receipt,
                "categories": receipts_by_category,
            },
            "expense": {
                "total": total_expense,
                "categories": expenses_by_category,
            },
            "balance": balance,
        }

    def _get_receipts_by_category(
        self, receipts: QuerySet[Transaction], total_receipt: float
    ) -> list:
        values_qs = receipts.values("category__name", "amount")
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
                "percentual": self._calculate_percentual(total, total_receipt),
            }
            for category_name, total in receipts_by_category_dict.items()
        ]

        return receipts_by_category

    def _get_expenses_by_category(
        self, expenses: QuerySet[Transaction], total_expense: float
    ) -> list:
        values_qs = expenses.values("category__name", "amount")
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
                "percentual": self._calculate_percentual(total, total_expense),
            }
            for category_name, total in expenses_by_category_dict.items()
        ]

        return expsenses_by_category

    def _calculate_percentual(self, category_value, total_value):
        if total_value == 0:
            return 100

        return round(category_value / total_value * 100, 2)

    def get_family(self, user: User) -> Family:
        return Family.objects.filter(
            members=user,
        ).first()

    def get_family_members(self, family: Family) -> dict:
        family_members = dict()
        for member in family.members.all():
            family_members[member.first_name] = member
        
        return family_members

    def get_accounts(self, family: Family) -> dict:
        accounts = Account.objects.filter(
            user_in=family.members.all(),
        )
        accounts_dict = dict()

        for account in accounts:
            accounts_dict[account.name] = account

        return accounts_dict

    def get_credit_cards(self, family: Family) -> dict:
        credit_cards = CreditCard.objects.filter(
            user_in=family.members.all(),
        )
        credit_cards_dict = dict()

        for credit_card in credit_cards:
            credit_cards_dict[credit_card.name] = credit_card

        return credit_cards_dict
    
    def get_category_names(self, family: Family) -> dict:
        categories = Category.objects.filter(
            user_in=family.members.all(),
        )
        category_names = dict()

        for category in categories:
            category_names[category.name] = category

        return category_names
    
    