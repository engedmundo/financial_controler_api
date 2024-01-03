import factory
from faker import Faker

from apps.account_manager.models.credit_card import CreditCard
from apps.account_manager.tests.factories.bank_factory import BankFactory
from apps.core.tests.factories.user_factory import UserFactory

fake = Faker("pt_BR")


class CreditCardFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    bank = factory.SubFactory(BankFactory)
    name = fake.company()
    expense_limit = fake.random_int(min=1000, max=20000)
    payment_day = fake.random_int(min=1, max=31)

    class Meta:
        model = CreditCard
