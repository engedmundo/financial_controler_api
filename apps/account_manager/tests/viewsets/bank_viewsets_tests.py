from rest_framework import status
from rest_framework.test import APIClient

from apps.account_manager.tests.factories import BankFactory
from apps.core.tests.base_test import BaseTest


class BankViewSetTest(BaseTest):
    def test_get_banks_authenticated(self):
        # Given
        bank_1 = BankFactory()
        bank_2 = BankFactory()
        expected_data = [
            {"id": bank.id, "name": bank.name, "code": bank.code}
            for bank in [bank_1, bank_2]
        ]

        # When
        response = self.auth_client.get("/api/banks/")
        response_data = response.data

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["id"], bank_1.id)
        self.assertEqual(response_data[1]["id"], bank_2.id)

    def test_get_banks_unauthenticated(self):
        # Given
        expected_message = "As credenciais de autenticação não foram fornecidas."

        # When
        response = APIClient().get("/api/banks/")

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], expected_message)
