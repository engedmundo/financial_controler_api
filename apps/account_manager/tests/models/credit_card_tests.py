import pytest

from apps.account_manager.models import CreditCard
from apps.account_manager.tests.factories import CreditCardFactory
from apps.core.tests.base_test import BaseModelsTest


class CreditCardModelTests(BaseModelsTest):
    def test_create_credit_card_model_instance(self):
        # Given
        expected_attrs = [
            "user",
            "bank",
            "name",
            "expense_limit",
            "payment_day",
            "created_at",
            "updated_at",
            "id",
        ]

        # When
        card = CreditCardFactory()
        db_cards = CreditCard.objects.all()
        db_card = db_cards.first()

        # Then
        self.assertIsInstance(card, CreditCard)
        self.assertEqual(len(db_cards), 1)
        self.assertEqual(str(db_card), card.name)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(card, attr_name)
                card_attr = getattr(card, attr_name)
                db_card_attr = getattr(db_card, attr_name)
                self.assertEqual(card_attr, db_card_attr)

    def test_credit_card_model_meta_verbose_names(self):
        # Then
        self.assertEqual(CreditCard._meta.verbose_name, "Cartão de crédito")
        self.assertEqual(
            CreditCard._meta.verbose_name_plural, "Cartões de crédito"
        )


@pytest.mark.parametrize("attr_name", ["user", "bank", "name", "payment_day"])
def test_credit_card_create_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with CreditCardModelTests().assertRaises(Exception):
        CreditCard.objects.create(**test_data)
