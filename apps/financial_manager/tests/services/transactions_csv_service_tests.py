from apps.core.tests.base_test import BaseTest
from apps.financial_manager.models import Transaction
from apps.financial_manager.services.transaction_csv_service import TransactionCSVService
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)
from apps.family_manager.tests.factories.family_factory import FamilyFactory


class TransactionCSVServiceTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.fixtures = TransactionsFixtures(self.user)
        self.fixtures.create_basic_instances()


    def test_if_service_is_successfully_instantiated_without_family(self):
        # Given
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id, 
        }

        # When
        service = TransactionCSVService(self.user, request_data_fixture)

        # Then
        self.assertIsInstance(service, TransactionCSVService)
        self.assertEqual(service.user, self.user)
        self.assertEqual(service.request_data, request_data_fixture)
        self.assertEqual(service.account, self.fixtures.account)
        self.assertEqual(service.credit_card, self.fixtures.card)
        self.assertEqual(service.family, None)
        self.assertIsInstance(service.categories_map, dict)
        self.assertEqual(service.categories_map[self.fixtures.category.name], self.fixtures.category)

    def test_if_service_is_successfully_instantiated_with_family(self):
        # Given
        family = FamilyFactory()
        family.members.set([self.user])
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id, 
        }

        # When
        service = TransactionCSVService(self.user, request_data_fixture)

        # Then
        self.assertIsInstance(service, TransactionCSVService)
        self.assertEqual(service.user, self.user)
        self.assertEqual(service.request_data, request_data_fixture)
        self.assertEqual(service.account, self.fixtures.account)
        self.assertEqual(service.credit_card, self.fixtures.card)
        self.assertEqual(service.family, family)
        self.assertIsInstance(service.categories_map, dict)
        self.assertEqual(service.categories_map[self.fixtures.category.name], self.fixtures.category)

