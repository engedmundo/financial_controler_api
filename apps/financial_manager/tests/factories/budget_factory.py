import random

import factory
from faker import Faker

from apps.core.tests.factories.user_factory import UserFactory
from apps.financial_manager.enums import FinancialTypeEnum, MonthEnum
from apps.financial_manager.models.budget import Budget
from apps.financial_manager.tests.factories.category_factory import (
    CategoryFactory,
)

fake = Faker("pt_BR")


class BudgetFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    month = random.choice(list(MonthEnum))
    year = fake.random_int(min=2023, max=2050)
    type = random.choice(list(FinancialTypeEnum))
    description = fake.sentence()

    class Meta:
        model = Budget
