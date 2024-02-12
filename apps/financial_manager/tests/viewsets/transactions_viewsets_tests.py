from rest_framework import status
from rest_framework.test import APIClient

from apps.account_manager.tests.factories import AccountFactory, CreditCardFactory
from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories.user_factory import UserFactory
from apps.financial_manager.tests.factories.category_factory import CategoryFactory
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)

TEST_ENDPOINT = "/api/transactions/"


class TransactionViewSetTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.fixtures = TransactionsFixtures(self.user)
        self.fixtures.create_basic_instances()

    def test_get_transactions(self):
        # Given
        expense = self.fixtures.create_expense_transaction()
        receipt = self.fixtures.create_receipt_transaction()

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
        self.assertListEqual(
            list(listed_item_1["user"].keys()),
            expected_user_keys,
        )
        self.assertListEqual(
            list(listed_item_1["account"].keys()),
            expected_account_keys,
        )
        self.assertListEqual(
            list(listed_item_1["credit_card"].keys()),
            expected_credit_card_keys,
        )
        self.assertListEqual(
            list(listed_item_1["category"].keys()),
            expected_category_keys,
        )

    def test_get_transactions_unauthenticated(self):
        # Given
        expected_message = "As credenciais de autenticação não foram fornecidas."

        # When
        response = APIClient().get(TEST_ENDPOINT)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], expected_message)

    def test_post_transaction_successfully(self):
        # Given
        payload = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "category": self.fixtures.category.id,
            "amount": 100.0,
            "date": "2021-01-01",
            "type": "expense",
            "description": "Test transaction",
        }
        expected_message = "Transação criada com sucesso"
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

        # When
        response = self.auth_client.post(TEST_ENDPOINT, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], expected_message)
        self.assertListEqual(
            list(response.data["transaction"].keys()), expected_main_keys
        )
        self.assertEqual(
            response.data["transaction"]["account"]["id"],
            self.fixtures.account.id,
        )
        self.assertEqual(
            response.data["transaction"]["credit_card"]["id"],
            self.fixtures.card.id,
        )
        self.assertEqual(
            response.data["transaction"]["category"]["id"],
            self.fixtures.category.id,
        )
        self.assertEqual(response.data["transaction"]["amount"], "100.00")
        self.assertEqual(response.data["transaction"]["date"], "2021-01-01")
        self.assertEqual(response.data["transaction"]["type"], "expense")
        self.assertEqual(
            response.data["transaction"]["description"], "Test transaction"
        )

    def test_post_transaction_successfully_without_account_card(self):
        # Given
        payload = {
            "category": self.fixtures.category.id,
            "amount": 100.0,
            "date": "2021-01-01",
            "type": "expense",
            "description": "Test transaction",
        }
        expected_message = "Transação criada com sucesso"
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

        # When
        response = self.auth_client.post(TEST_ENDPOINT, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], expected_message)
        self.assertListEqual(
            list(response.data["transaction"].keys()), expected_main_keys
        )
        self.assertIsNone(response.data["transaction"]["account"])
        self.assertIsNone(response.data["transaction"]["credit_card"])
        self.assertEqual(
            response.data["transaction"]["category"]["id"],
            self.fixtures.category.id,
        )
        self.assertEqual(response.data["transaction"]["amount"], "100.00")
        self.assertEqual(response.data["transaction"]["date"], "2021-01-01")
        self.assertEqual(response.data["transaction"]["type"], "expense")
        self.assertEqual(
            response.data["transaction"]["description"], "Test transaction"
        )

    def test_post_transaction_with_wrong_account_id(self):
        # Given
        other_user = UserFactory()
        other_account = AccountFactory(user=other_user)

        payload = {
            "account": other_account.id,
            "credit_card": self.fixtures.card.id,
            "category": self.fixtures.category.id,
            "amount": 100.0,
            "date": "2021-01-01",
            "type": "expense",
            "description": "Test transaction",
        }
        expected_message = "Conta não encontrada"

        # When
        response = self.auth_client.post(TEST_ENDPOINT, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], expected_message)

    def test_post_transaction_with_wrong_credit_card_id(self):
        # Given
        other_user = UserFactory()
        other_card = CreditCardFactory(user=other_user)

        payload = {
            "account": self.fixtures.account.id,
            "credit_card": other_card.id,
            "category": self.fixtures.category.id,
            "amount": 100.0,
            "date": "2021-01-01",
            "type": "expense",
            "description": "Test transaction",
        }
        expected_message = "Cartão de crédito não encontrado"

        # When
        response = self.auth_client.post(TEST_ENDPOINT, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], expected_message)

    def test_post_transaction_with_wrong_category_id(self):
        # Given
        other_user = UserFactory()
        other_category = CategoryFactory(user=other_user)

        payload = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "category": other_category.id,
            "amount": 100.0,
            "date": "2021-01-01",
            "type": "expense",
            "description": "Test transaction",
        }
        expected_message = "Categoria não encontrada"

        # When
        response = self.auth_client.post(TEST_ENDPOINT, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], expected_message)

    def test_post_transaction_with_transaction_already_registered(self):
        # Given
        expense = self.fixtures.create_expense_transaction()

        payload = {
            "account": expense.account.id,
            "credit_card": expense.credit_card.id,
            "category": expense.category.id,
            "amount": expense.amount,
            "date": expense.date,
            "type": expense.type,
            "description": expense.description,
        }
        expected_message = "Transação atualizada com sucesso"

        # When
        response = self.auth_client.post(TEST_ENDPOINT, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], expected_message)
