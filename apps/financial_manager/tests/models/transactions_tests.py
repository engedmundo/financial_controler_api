import pytest

from apps.account_manager.tests.factories import (
    AccountFactory,
    CreditCardFactory,
)
from apps.core.tests.base_test import BaseModelsTest
from apps.financial_manager.models import Transaction
from apps.financial_manager.tests.factories import (
    CategoryFactory,
    TransactionFactory,
)


class TransactionModelTests(BaseModelsTest):
    def test_create_transaction_model_instance(self):
        # Given
        expected_attrs = [
            "user",
            "account",
            "credit_card",
            "category",
            "amount",
            "date",
            "description",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        category = CategoryFactory()
        account = AccountFactory(user=category.user)
        card = CreditCardFactory(user=category.user)
        transaction = TransactionFactory(
            user=category.user,
            account=account,
            credit_card=card,
            category=category,
        )
        db_transactions = Transaction.objects.all()
        db_transaction = db_transactions.first()

        # Then
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(len(db_transactions), 1)
        self.assertEqual(str(db_transaction), transaction.description)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(transaction, attr_name)
                transaction_attr = getattr(transaction, attr_name)
                db_transaction_attr = getattr(db_transaction, attr_name)

                if attr_name == "date":
                    db_transaction_attr = db_transaction_attr.strftime(
                        "%Y-%m-%d"
                    )

                self.assertEqual(transaction_attr, db_transaction_attr)

    def test_transaction_model_meta_verbose_names(self):
        # Then
        self.assertEqual(Transaction._meta.verbose_name, "Transação")
        self.assertEqual(Transaction._meta.verbose_name_plural, "Transações")


@pytest.mark.parametrize(
    "attr_name", ["user", "category", "amount", "date", "type", "description"]
)
def test_create_transaction_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with TransactionModelTests().assertRaises(Exception):
        Transaction.objects.create(**test_data)
