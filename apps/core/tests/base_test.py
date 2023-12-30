from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class BaseModelsTest(TestCase):
    def assertHasAttr(self, obj, attr):
        self.assertTrue(hasattr(obj, attr), f"{obj.__class__.__name__} does not have attribute {attr}")
    

class BaseTest(TestCase):
    def setUp(self):
        self.user = self.create_test_user()
        self.auth_client = self.create_authenticated_client()

    def create_test_user(self, username="testuser", password="testpassword"):
        return User.objects.create_user(
            username=username,
            password=password,
        )

    def create_authenticated_client(self, user=None):
        client = APIClient()
        user = user or self.user
        client.force_authenticate(user=user)
        return client
