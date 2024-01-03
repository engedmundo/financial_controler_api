import random

import factory
from faker import Faker

from apps.account_manager.models.account_history import AccountHistory
from apps.account_manager.tests.factories.bank_factory import BankFactory
from apps.core.tests.factories.user_factory import UserFactory

fake = Faker("pt_BR")


class AccountHistoryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(BankFactory)
    date = fake.date()
    balance = fake.random_int(min=-20000, max=20000)

    class Meta:
        model = AccountHistory
