from rest_framework import status
from rest_framework.test import APIClient

from apps.account_manager.tests.factories import AccountFactory, CreditCardFactory
from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories.user_factory import UserFactory
from apps.family_manager.tests.factories.family_factory import FamilyFactory
from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.tests.factories import TransactionFactory
from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)

TEST_ENDPOINT = "/api/transactions/family/"


class TransactionByFamilyViewSetTest(BaseTest):
    def setUp(self):
        super().setUp()
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        self.expense_1 = fixtures.create_expense_transaction()
        self.receipt_1 = fixtures.create_receipt_transaction()

        # other family member data
        self.family_member = UserFactory()
        self.account_fm = AccountFactory(user=self.family_member, bank=fixtures.bank)
        self.card_fm = CreditCardFactory(user=self.family_member, bank=fixtures.bank)
        self.expense_2 = TransactionFactory(
            user=self.family_member,
            account=self.account_fm,
            credit_card=self.card_fm,
            category=fixtures.category,
            type=FinancialTypeEnum.EXPENSE,
        )
        self.receipt_2 = TransactionFactory(
            user=self.family_member,
            account=self.account_fm,
            credit_card=self.card_fm,
            category=fixtures.category,
            type=FinancialTypeEnum.RECEIPT,
        )
        # create family and set members family
        self.family = FamilyFactory()
        self.family.members.set([self.user, self.family_member])

    def test_get_transactions_by_family(self):
        # Given
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
        expected_transactions_ids = set(
            [self.expense_1.id, self.receipt_1.id, self.expense_2.id, self.receipt_2.id]
        )

        # When
        response = self.auth_client.get(f"{TEST_ENDPOINT}{self.family.id}/")
        response_transactions_data = response.data["transactions"]
        response_summary_data = response.data["summary"]
        listed_item_1 = response_transactions_data[0]
        obtained_transactions_ids = set(
            [item["id"] for item in response_transactions_data]
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_transactions_data), 4)
        self.assertSetEqual(expected_transactions_ids, obtained_transactions_ids)
        self.assertListEqual(list(listed_item_1.keys()), expected_main_keys)
        self.assertListEqual(list(listed_item_1["user"].keys()), expected_user_keys)
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
        self.assertListEqual(
            list(listed_item_1["category"].keys()),
            expected_category_keys,
        )
        self.assertListEqual(list(response_summary_data.keys()), expected_summary_keys)

    def test_get_transactions_by_family_whitout_family(self):
        # Given
        expected_message = "Família não encontrada"

        # When
        response = self.auth_client.get(f"{TEST_ENDPOINT}99/")

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], expected_message)

    def test_get_transactions_by_family_unauthenticated(self):
        # Given
        expected_message = "As credenciais de autenticação não foram fornecidas."

        # When
        response = APIClient().get(f"{TEST_ENDPOINT}{self.family.id}/")

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], expected_message)
