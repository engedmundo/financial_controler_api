import factory
from faker import Faker

from apps.family_manager.models.family import Family

fake = Faker("pt_BR")


class FamilyFactory(factory.django.DjangoModelFactory):
    name = fake.company()

    class Meta:
        model = Family
