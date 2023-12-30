from factory import Factory
from faker import Faker

from apps.account_manager.models.bank import Bank

fake = Faker('pt_BR')

class BankFactory(Factory):
    class Meta:
        model = Bank

    name = fake.company()
    code = fake.random_number(digits=3)
    