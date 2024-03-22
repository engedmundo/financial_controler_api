from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories.user_factory import UserFactory
from apps.financial_manager.tests.factories.category_factory import (
    CategoryFactory,
)
from apps.financial_manager.tests.fixtures.category_fixtures import (
    CategoryFixtures,
)

TEST_ENDPOINT = "/api/categories/"


class CategoryViewSetTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.fixtures = CategoryFixtures(self.user)
        self.fixtures.create_basic_instances()

    def test_get_categories(self):
        # Given in setUp

        expected_main_keys = [
            "id",
            "name",
            "description",
        ]

        # When
        response = self.auth_client.get(TEST_ENDPOINT)
        response_data = response.data
        listed_item_0 = response_data[0]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertListEqual(list(listed_item_0.keys()), expected_main_keys)
        self.assertEqual(listed_item_0["id"], self.fixtures.category.id)
        self.assertEqual(listed_item_0["name"], self.fixtures.category.name)
        self.assertEqual(
            listed_item_0["description"],
            self.fixtures.category.description,
        )

    def test_category_returns_categories_from_family_memeber(self):
        # Given
        other_user = UserFactory()
        other_category = CategoryFactory(user=other_user)
        self.fixtures.family.members.add(other_user)

        # When
        response = self.auth_client.get(TEST_ENDPOINT)
        response_data = response.data
        listed_item_0 = response_data[0]
        listed_item_1 = response_data[1]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(listed_item_0["id"], self.fixtures.category.id)
        self.assertEqual(listed_item_0["name"], self.fixtures.category.name)
        self.assertEqual(
            listed_item_0["description"],
            self.fixtures.category.description,
        )
        self.assertEqual(listed_item_1["id"], other_category.id)
        self.assertEqual(listed_item_1["name"], other_category.name)
        self.assertEqual(
            listed_item_1["description"],
            other_category.description,
        )

    def test_category_returns_only_user_categories(self):
        # Given
        other_user = UserFactory()
        other_category = CategoryFactory(user=other_user)
        auth_client = self.create_authenticated_client(user=other_user)

        # When
        response = auth_client.get(TEST_ENDPOINT)
        response_data = response.data
        listed_item_0 = response_data[0]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(listed_item_0["id"], other_category.id)
        self.assertEqual(listed_item_0["name"], other_category.name)
        self.assertEqual(
            listed_item_0["description"],
            other_category.description,
        )
