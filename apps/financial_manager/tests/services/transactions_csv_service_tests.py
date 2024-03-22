from io import BytesIO

import pandas as pd

from apps.core.tests.base_test import BaseTest
from apps.family_manager.tests.factories.family_factory import FamilyFactory
from apps.financial_manager.models import Transaction
from apps.financial_manager.services.transaction_csv_service import (
    TransactionCSVService,
)
from apps.financial_manager.tests.factories.category_factory import (
    CategoryFactory,
)
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)


class TransactionCSVServiceTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.fixtures = TransactionsFixtures(self.user)
        self.fixtures.create_basic_instances()
        self.csv_data = """date,description,amount,category,type\n14/11/2023,Antecipada - Amazon Marketplace - 3/8,"50,53",Compras Gerais,expense\n14/11/2023,Amazon Marketplace - 2/8,"50,53",Compras Gerais,expense\n14/11/2023,Alura *Alura - Plus - 7/12/2023,"92,65",Compras Gerais,expense"""

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
        self.assertEqual(
            service.categories_map[self.fixtures.category.name],
            self.fixtures.category,
        )

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
        self.assertEqual(
            service.categories_map[self.fixtures.category.name],
            self.fixtures.category,
        )

    def test_get_file_content_df(self):
        # Given
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "csv_file": BytesIO(self.csv_data.encode()),
        }
        expected_columns = ["date", "description", "amount", "category", "type"]

        # When
        service = TransactionCSVService(self.user, request_data_fixture)
        resp_df = service.get_file_content_df()

        # Then
        self.assertIsInstance(resp_df, pd.DataFrame)
        self.assertListEqual(list(resp_df.columns), expected_columns)

    def test_treat_content_df(self):
        # Given
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "csv_file": BytesIO(self.csv_data.encode()),
        }
        expected_keys = [
            "date",
            "description",
            "amount",
            "category",
            "type",
            "user",
            "account",
            "credit_card",
        ]

        # When
        service = TransactionCSVService(self.user, request_data_fixture)
        transactions_df = service.get_file_content_df()
        resp = service.treat_content_df(transactions_df)
        first_item = resp[0]

        # Then
        self.assertIsInstance(resp, list)
        self.assertEqual(len(resp), 3)
        self.assertListEqual(list(first_item.keys()), expected_keys)
        self.assertEqual(first_item["date"], "2023-11-14")
        self.assertEqual(
            first_item["description"], "Antecipada - Amazon Marketplace - 3/8"
        )
        self.assertEqual(first_item["amount"], 50.53)
        self.assertEqual(first_item["category"], "Compras Gerais")
        self.assertEqual(first_item["type"], "expense")
        self.assertEqual(first_item["user"], self.user)
        self.assertEqual(first_item["account"], self.fixtures.account)
        self.assertEqual(first_item["credit_card"], self.fixtures.card)

    def test_create_or_update_transactions(self):
        # Given
        new_category = CategoryFactory(user=self.user, name="Compras Gerais")
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "csv_file": BytesIO(self.csv_data.encode()),
        }
        expected_keys = ["saved_registers", "failed_registers"]

        # When
        service = TransactionCSVService(self.user, request_data_fixture)
        transactions_df = service.get_file_content_df()
        transactions = service.treat_content_df(transactions_df)
        resp = service.create_or_update_transactions(transactions)
        transactions_new_category = Transaction.objects.filter(
            user=self.user, category=new_category
        )

        # Then
        self.assertIsInstance(resp, dict)
        self.assertListEqual(list(resp.keys()), expected_keys)
        self.assertEqual(resp["saved_registers"], 3)
        self.assertEqual(len(transactions_new_category), 3)
        self.assertEqual(resp["failed_registers"], list())

    def test_create_or_update_transactions_when_missing_category(self):
        # Given
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "csv_file": BytesIO(self.csv_data.encode()),
        }
        expected_keys = ["saved_registers", "failed_registers"]
        expected_error_keys = ["date", "description", "amount", "error"]

        # When
        service = TransactionCSVService(self.user, request_data_fixture)
        transactions_df = service.get_file_content_df()
        transactions = service.treat_content_df(transactions_df)
        resp = service.create_or_update_transactions(transactions)
        first_error_item = resp["failed_registers"][0]

        # Then
        self.assertIsInstance(resp, dict)
        self.assertListEqual(list(resp.keys()), expected_keys)
        self.assertListEqual(list(first_error_item.keys()), expected_error_keys)
        self.assertEqual(resp["saved_registers"], 0)
