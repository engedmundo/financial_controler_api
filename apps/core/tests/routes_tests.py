from unittest import TestCase

from django.urls import reverse


class AuthURLTest(TestCase):
    def test_token_obtain_pair_url_resolves(self):
        url = reverse("token_obtain_pair")
        self.assertEqual(url, "/api/token/")

    def test_token_refresh_url_resolves(self):
        url = reverse("token_refresh")
        self.assertEqual(url, "/api/token/refresh/")

    def test_token_verify_url_resolves(self):
        url = reverse("token_verify")
        self.assertEqual(url, "/api/token/verify/")
