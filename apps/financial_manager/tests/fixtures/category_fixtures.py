from apps.family_manager.tests.factories import FamilyFactory
from apps.financial_manager.tests.factories import CategoryFactory


class CategoryFixtures:
    def __init__(self, user) -> None:
        self.user = user

    def create_basic_instances(self) -> None:
        self.category = CategoryFactory(user=self.user)
        self.family = FamilyFactory()
        self.family.members.add(self.user)
