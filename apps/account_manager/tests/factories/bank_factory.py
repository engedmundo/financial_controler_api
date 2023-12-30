import factory
from faker import Faker

from apps.account_manager.models.bank import Bank

fake = Faker('pt_BR')

class BankFactory(factory.django.DjangoModelFactory):
    name = fake.company()
    code = fake.random_number(digits=3)

    class Meta:
        model = Bank