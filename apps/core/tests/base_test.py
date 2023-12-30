from django.contrib.auth.models import User
from django.test import TestCase


class BaseModelsTest(TestCase):
    def assertHasAttr(self, obj, attr):
        self.assertTrue(hasattr(obj, attr), f"{obj.__class__.__name__} does not have attribute {attr}")
    

class BaseTest(TestCase):
    
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
