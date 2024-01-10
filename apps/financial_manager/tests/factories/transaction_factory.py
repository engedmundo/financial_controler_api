import random

import factory
from faker import Faker

from apps.account_manager.tests.factories import AccountFactory, CreditCardFactory
from apps.core.tests.factories.user_factory import UserFactory
from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.models.transaction import Transaction
from apps.financial_manager.tests.factories.category_factory import CategoryFactory

fake = Faker("pt_BR")


class TransactionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(AccountFactory)
    credit_card = factory.SubFactory(CreditCardFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    date = fake.date()
    type = random.choice(list(FinancialTypeEnum))
    description = fake.sentence()

    class Meta:
        model = Transaction
