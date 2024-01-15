from rest_framework import status
from rest_framework.test import APIClient

from apps.core.tests.base_test import BaseTest

from apps.financial_manager.tests.fixtures.transactions_fixtures import (
    TransactionsFixtures,
)
from apps.financial_manager.tests.factories.category_factory import CategoryFactory
from django.core.files.uploadedfile import SimpleUploadedFile

TEST_ENDPOINT = "/api/transactions/csv/"


class TransactionCSVViewSetTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.fixtures = TransactionsFixtures(self.user)
        self.fixtures.create_basic_instances()
        new_category = CategoryFactory(user=self.user, name="Compras Gerais")
        self.csv_data = b"""date,description,amount,category,type\n14/11/2023,Antecipada - Amazon Marketplace - 3/8,"50,53",Compras Gerais,expense\n14/11/2023,Amazon Marketplace - 2/8,"50,53",Compras Gerais,expense\n14/11/2023,Alura *Alura - Plus - 7/12/2023,"92,65",Compras Gerais,expense"""

    def test_post_csv_transactions(self):
        # Given
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
            "csv_file": SimpleUploadedFile("file.csv", self.csv_data),
        }

        expected_main_keys = [
            "saved_registers",
            "failed_registers",
        ]

        # When
        response = self.auth_client.post(
            TEST_ENDPOINT,
            data=request_data_fixture,
            format="multipart",
        )
        response_data = response.data

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["saved_registers"], 3)
        self.assertListEqual(response_data["failed_registers"], list())

    def test_post_csv_transactions_without_file(self):
        # Given
        fixtures = TransactionsFixtures(self.user)
        fixtures.create_basic_instances()
        request_data_fixture = {
            "account": self.fixtures.account.id,
            "credit_card": self.fixtures.card.id,
        }
        expected_message = "Um arquivo *.csv deve ser enviado"

        # When
        response = self.auth_client.post(
            TEST_ENDPOINT,
            data=request_data_fixture,
            format="multipart",
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], expected_message)

    def test_post_csv_transactions_unauthenticated(self):
        # Given
        expected_message = "As credenciais de autenticação não foram fornecidas."

        # When
        response = APIClient().post(TEST_ENDPOINT)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], expected_message)
