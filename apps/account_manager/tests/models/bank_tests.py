import pytest

from apps.account_manager.models import Bank
from apps.account_manager.tests.factories import BankFactory
from apps.core.tests.base_test import BaseModelsTest


class BankModelTests(BaseModelsTest):
    def test_create_bank_model_instance(self):
        # Given
        expected_attrs = [
            "name",
            "code",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        bank = BankFactory()
        db_banks = Bank.objects.all()
        db_bank = db_banks.first()

        # Then
        self.assertIsInstance(bank, Bank)
        self.assertEqual(len(db_banks), 1)
        self.assertEqual(str(bank), bank.name)
        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(bank, attr_name)
                bank_attr = getattr(bank, attr_name)
                db_bank_attr = getattr(db_bank, attr_name)
                self.assertEqual(bank_attr, db_bank_attr)

    def test_bank_model_meta_verbose_names(self):
        # Then
        self.assertEqual(Bank._meta.verbose_name, "Banco")
        self.assertEqual(Bank._meta.verbose_name_plural, "Bancos")


@pytest.mark.parametrize("attr_name", ["name", "code"])
def test_bank_create_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with BankModelTests().assertRaises(Exception):
        Bank.objects.create(**test_data)
