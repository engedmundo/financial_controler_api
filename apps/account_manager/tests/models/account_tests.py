import pytest

from apps.account_manager.models import Account
from apps.account_manager.tests.factories import AccountFactory
from apps.core.tests.base_test import BaseModelsTest


class AccountModelTests(BaseModelsTest):
    def test_create_account_model_instance(self):
        # Given
        expected_attrs = [
            "user",
            "bank",
            "name",
            "agency",
            "number",
            "type",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        account = AccountFactory()
        db_accounts = Account.objects.all()
        db_account = db_accounts.first()

        # Then
        self.assertIsInstance(account, Account)
        self.assertEqual(len(db_accounts), 1)
        self.assertEqual(str(db_account), account.name)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(account, attr_name)
                account_attr = getattr(account, attr_name)
                db_account_attr = getattr(db_account, attr_name)
                self.assertEqual(account_attr, db_account_attr)

    def test_account_model_meta_verbose_names(self):
        # Then
        self.assertEqual(Account._meta.verbose_name, "Conta")
        self.assertEqual(Account._meta.verbose_name_plural, "Contas")


@pytest.mark.parametrize(
    "attr_name", ["user", "bank", "name", "agency", "number", "type"]
)
def test_account_create_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with AccountModelTests().assertRaises(Exception):
        Account.objects.create(**test_data)
