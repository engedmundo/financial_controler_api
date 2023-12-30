from apps.core.tests.base_test import BaseModelsTest

from apps.account_manager.models import Bank
from apps.account_manager.tests.factories import BankFactory


class BankModelTests(BaseModelsTest):
    def test_create_bank_model_instance(self):
        # Given
        expected_name = "Example Bank"
        expected_code = "EXB"
        expected_attrs = [
            "name",
            "code",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        bank_instance = BankFactory(
            name=expected_name, 
            code=expected_code,
        )

        # Then
        self.assertEqual(bank_instance.name, expected_name)
        self.assertEqual(bank_instance.code, expected_code)
        self.assertIsInstance(bank_instance, Bank)
        for attr in expected_attrs:
            with self.subTest(attr=attr):
                self.assertHasAttr(bank_instance, attr)