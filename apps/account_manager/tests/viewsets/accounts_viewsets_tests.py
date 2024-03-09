from rest_framework import status
from rest_framework.test import APIClient

from apps.account_manager.tests.factories import AccountFactory
from apps.core.tests.base_test import BaseTest

TEST_ENDPOINT = "/api/accounts/"


class AccountViewSetTest(BaseTest):
    def test_get_accounts(self):
        # Given
        account_1 = AccountFactory(user=self.user)
        account_2 = AccountFactory(user=self.user)
        expected_main_keys = [
            "id",
            "name",
            "agency",
            "number",
            "type",
            "user",
            "bank",
        ]
        expected_user_keys = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]
        expected_bank_keys = [
            "id",
            "name",
            "code",
        ]

        # When
        response = self.auth_client.get(TEST_ENDPOINT)
        response_data = response.data
        listed_item_1 = response_data[0]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["id"], account_1.id)
        self.assertEqual(response_data[1]["id"], account_2.id)
        self.assertListEqual(list(listed_item_1.keys()), expected_main_keys)
        self.assertListEqual(
            list(listed_item_1["user"].keys()), expected_user_keys
        )
        self.assertListEqual(
            list(listed_item_1["bank"].keys()), expected_bank_keys
        )

    def test_get_accounts_unauthenticated(self):
        # Given
        expected_message = (
            "As credenciais de autenticação não foram fornecidas."
        )

        # When
        response = APIClient().get(TEST_ENDPOINT)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], expected_message)
