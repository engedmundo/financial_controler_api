from apps.core.tests.base_test import BaseTest
from apps.financial_manager.models import Transaction
from apps.financial_manager.services.transaction_service import TransactionService
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)


class TransactionCSVServiceTest(BaseTest):
    def test_if_service_is_successfully_instantiated(self):
        # Given

        # When
        service = TransactionService()

        # Then
        self.assertIsInstance(service, TransactionService)
