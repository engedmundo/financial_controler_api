from apps.core.tests.base_test import BaseTest
from apps.financial_manager.models import Transaction
from apps.financial_manager.services.transaction_service import TransactionService
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)


class TransactionServiceTest(BaseTest):
    def setUp(self):
        super().setUp()
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        self.expense = fixtures.create_expense_transaction()
        self.receipt = fixtures.create_receipt_transaction()
        self.transactions = Transaction.objects.filter(user=self.user)

    def test_if_service_is_successfully_instantiated(self):
        # Given

        # When
        service = TransactionService(self.transactions)

        # Then
        self.assertIsInstance(service, TransactionService)
        self.assertEqual(len(service.receipts), 1)
        self.assertEqual(len(service.expenses), 1)
        self.assertEqual(service.total_receipt, 0)
        self.assertEqual(service.total_expense, 0)

    def test_get_receipts_by_category(self):
        # Given
        service = TransactionService(self.transactions)
        expected_keys = ["category", "total", "percentual"]

        # When
        resp = service._get_receipts_by_category()
        receipt = resp[0]

        # Then
        self.assertEqual(len(resp), 1)
        self.assertListEqual(list(receipt.keys()), expected_keys)
        self.assertEqual(receipt["percentual"], 100)

    def test_get_expenses_by_category(self):
        # Given
        service = TransactionService(self.transactions)
        expected_keys = ["category", "total", "percentual"]

        # When
        resp = service._get_expenses_by_category()
        receipt = resp[0]

        # Then
        self.assertEqual(len(resp), 1)
        self.assertListEqual(list(receipt.keys()), expected_keys)
        self.assertEqual(receipt["percentual"], 100)

    def test_get_transaction_summary_successfuly(self):
        # Given
        service = TransactionService(self.transactions)
        expected_balance = self.receipt.amount - self.expense.amount
        expected_main_keys = ["receipt", "expense", "balance"]
        expected_secondary_keys = ["total", "categories"]

        # When
        resp = service.get_transactions_summary()

        # Then
        self.assertEqual(resp["receipt"]["total"], self.receipt.amount)
        self.assertEqual(resp["expense"]["total"], self.expense.amount)
        self.assertEqual(resp["balance"], expected_balance)
        self.assertListEqual(list(resp.keys()), expected_main_keys)
        self.assertListEqual(list(resp["receipt"].keys()), expected_secondary_keys)

    def test_get_transaction_summary_without_data(self):
        # Given
        Transaction.objects.all().delete()
        queryset = Transaction.objects.all()
        service = TransactionService(queryset)

        # When
        resp = service.get_transactions_summary()

        # Then
        self.assertEqual(resp["receipt"]["total"], 0)
        self.assertEqual(resp["expense"]["total"], 0)
        self.assertEqual(resp["balance"], 0)
        self.assertListEqual(resp["receipt"]["categories"], list())
        self.assertListEqual(resp["expense"]["categories"], list())

    def test_calculate_percentual_returns_100(self):
        # Given
        total_value = 0
        category_value = 100

        # When
        service = TransactionService(self.transactions)
        resp = service._calculate_percentual(category_value, total_value)

        # Then
        self.assertEqual(resp, 100)

    def test_calculate_percentual_when_total_value_isnt_zero(self):
        # Given
        total_value = 500
        category_value = 100

        # When
        service = TransactionService(self.transactions)
        resp = service._calculate_percentual(category_value, total_value)

        # Then
        self.assertEqual(resp, 20)
