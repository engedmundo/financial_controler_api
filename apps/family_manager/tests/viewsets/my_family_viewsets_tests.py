from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories.user_factory import UserFactory
from apps.family_manager.tests.factories.family_factory import FamilyFactory

TEST_ENDPOINT = "/api/my-family/"


class MyFamilyViewSetTest(BaseTest):
    def setUp(self):
        super().setUp()

        # other family member data
        self.family_member = UserFactory()

        # create family and set members family
        self.family = FamilyFactory()
        self.family.members.set([self.user, self.family_member])

    def test_get_my_family(self):
        # Given
        expected_main_keys = [
            "id",
            "name",
            "members",
        ]
        expected_members_keys = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]
        expected_family_id = self.family.id

        # When
        response = self.auth_client.get(f"{TEST_ENDPOINT}")
        response_data = response.data
        response_members = response_data["members"]
        member_0 = response_members[0]
        member_1 = response_members[1]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_family_id, response_data["id"])
        self.assertListEqual(list(response_data.keys()), expected_main_keys)
        self.assertListEqual(list(response_members[0].keys()), expected_members_keys)
        self.assertListEqual(list(response_members[1].keys()), expected_members_keys)
        self.assertEqual(member_0["id"], self.user.id)
        self.assertEqual(member_1["id"], self.family_member.id)
