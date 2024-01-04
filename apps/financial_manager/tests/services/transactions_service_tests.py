from apps.core.tests.base_test import BaseTest
from apps.financial_manager.models import Transaction
from apps.financial_manager.services.transaction_service import TransactionService
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)


class TransactionServiceTest(BaseTest):
    def test_if_service_is_successfully_instantiated(self):
        # Given

        # When
        service = TransactionService()

        # Then
        self.assertIsInstance(service, TransactionService)

    def test_get_transaction_summary_successfuly(self):
        # Given
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        expense = fixtures.create_expense_transaction()
        receipt = fixtures.create_receipt_transaction()
        expected_balance = receipt.amount - expense.amount

        # When
        transactions = Transaction.objects.filter(user=self.user)
        obtained_summary = TransactionService.get_transactions_summary(transactions)

        # Then
        self.assertEqual(obtained_summary["receipt"], receipt.amount)
        self.assertEqual(obtained_summary["expense"], expense.amount)
        self.assertEqual(obtained_summary["balance"], expected_balance)

    def test_get_transaction_summary_without_receipt_successfuly(self):
        # Given
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        expense = fixtures.create_expense_transaction()
        expected_balance = 0 - expense.amount

        # When
        transactions = Transaction.objects.filter(user=self.user)
        obtained_summary = TransactionService.get_transactions_summary(transactions)

        # Then
        self.assertEqual(obtained_summary["receipt"], 0)
        self.assertEqual(obtained_summary["expense"], expense.amount)
        self.assertEqual(obtained_summary["balance"], expected_balance)

    def test_get_transaction_summary_without_expense_successfuly(self):
        # Given
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        receipt = fixtures.create_receipt_transaction()
        expected_balance = receipt.amount - 0

        # When
        transactions = Transaction.objects.filter(user=self.user)
        obtained_summary = TransactionService.get_transactions_summary(transactions)

        # Then
        self.assertEqual(obtained_summary["receipt"], receipt.amount)
        self.assertEqual(obtained_summary["expense"], 0)
        self.assertEqual(obtained_summary["balance"], expected_balance)
