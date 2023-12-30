from apps.account_manager.models import Bank
from apps.account_manager.tests.factories import BankFactory
from apps.core.tests.base_test import BaseModelsTest


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
        self.assertEqual(str(bank_instance), "Example Bank")
        for attr in expected_attrs:
            with self.subTest(attr=attr):
                self.assertHasAttr(bank_instance, attr)

    def test_bank_model_meta_verbose_names(self):
        # Then
        self.assertEqual(Bank._meta.verbose_name, "Banco")
        self.assertEqual(Bank._meta.verbose_name_plural, "Bancos")

    def test_bank_fields_are_required(self):
        # Then
        with self.assertRaises(Exception):
            Bank.objects.create(name=None, code="EXB")
        # Then
        with self.assertRaises(Exception):
            Bank.objects.create(name="Example Bank", code=None)
