from apps.account_manager.tests.factories import (
    AccountFactory,
    BankFactory,
    CreditCardFactory,
)
from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.models import Transaction
from apps.financial_manager.tests.factories import CategoryFactory, TransactionFactory


class TransactionsFixtures:
    def __init__(self, user) -> None:
        self.user = user

    def create_basic_instances(self) -> None:
        self.bank = BankFactory()
        self.account = AccountFactory(user=self.user, bank=self.bank)
        self.card = CreditCardFactory(user=self.user, bank=self.bank)
        self.category = CategoryFactory(user=self.user)

    def create_expense_transaction(self) -> Transaction:
        return TransactionFactory(
            user=self.user,
            account=self.account,
            credit_card=self.card,
            category=self.category,
            type=FinancialTypeEnum.EXPENSE,
        )

    def create_receipt_transaction(self) -> Transaction:
        return TransactionFactory(
            user=self.user,
            account=self.account,
            credit_card=self.card,
            category=self.category,
            type=FinancialTypeEnum.RECEIPT,
        )
