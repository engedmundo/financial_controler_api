import factory
from django.contrib.auth.models import User
from faker import Faker

fake = Faker("pt_BR")


class UserFactory(factory.django.DjangoModelFactory):
    username = fake.user_name()
    password = fake.password()
    email = fake.email()

    class Meta:
        model = User
