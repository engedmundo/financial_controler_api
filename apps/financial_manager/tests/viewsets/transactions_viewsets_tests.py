from rest_framework import status
from rest_framework.test import APIClient

from apps.core.tests.base_test import BaseTest

from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)

TEST_ENDPOINT = "/api/transactions/"


class TransactionViewSetTest(BaseTest):
    def test_get_transactions(self):
        # Given
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        expense = fixtures.create_expense_transaction()
        receipt = fixtures.create_receipt_transaction()

        expected_main_keys = [
            "id",
            "user",
            "account",
            "credit_card",
            "category",
            "amount",
            "date",
            "type",
            "description",
        ]
        expected_user_keys = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]
        expected_account_keys = [
            "id",
            "name",
            "agency",
            "number",
            "type",
        ]
        expected_credit_card_keys = [
            "id",
            "name",
            "expense_limit",
            "payment_day",
        ]
        expected_category_keys = [
            "id",
            "name",
            "description",
        ]
        expected_summary_keys = [
            "receipt",
            "expense",
            "balance",
        ]

        # When
        response = self.auth_client.get(TEST_ENDPOINT)
        response_transactions_data = response.data["transactions"]
        response_summary_data = response.data["summary"]
        listed_item_1 = response_transactions_data[0]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_transactions_data), 2)
        self.assertEqual(response_transactions_data[0]["id"], expense.id)
        self.assertEqual(response_transactions_data[1]["id"], receipt.id)
        self.assertListEqual(list(listed_item_1.keys()), expected_main_keys)
        self.assertListEqual(list(listed_item_1["user"].keys()), expected_user_keys)
        self.assertListEqual(
            list(listed_item_1["account"].keys()), expected_account_keys
        )
        self.assertListEqual(
            list(listed_item_1["credit_card"].keys()), expected_credit_card_keys
        )
        self.assertListEqual(
            list(listed_item_1["category"].keys()), expected_category_keys
        )

    def test_get_transactions_unauthenticated(self):
        # Given
        expected_message = "As credenciais de autenticação não foram fornecidas."

        # When
        response = APIClient().get(TEST_ENDPOINT)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], expected_message)
