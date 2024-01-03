import factory
from faker import Faker

from apps.core.tests.factories.user_factory import UserFactory
from apps.financial_manager.models.category import Category

fake = Faker("pt_BR")


class CategoryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = fake.company()
    description = fake.sentence()

    class Meta:
        model = Category
