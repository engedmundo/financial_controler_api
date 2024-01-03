import random

import factory
from faker import Faker

from apps.account_manager.enums import AccountTypeEnum
from apps.account_manager.models.account import Account
from apps.account_manager.tests.factories.bank_factory import BankFactory
from apps.core.tests.factories.user_factory import UserFactory

fake = Faker("pt_BR")


class AccountFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    bank = factory.SubFactory(BankFactory)
    name = fake.company()
    agency = str(fake.random_number(digits=5))
    number = str(fake.random_number(digits=10))
    type = random.choice(list(AccountTypeEnum))

    class Meta:
        model = Account
