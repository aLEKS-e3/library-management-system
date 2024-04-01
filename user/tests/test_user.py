from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase


class UnauthorizedUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_manage_no_access(self):
        res = self.client.get(path=reverse("user:manage"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        payload = {"email": "test@test.com", "password": "test_password"}

        self.user = get_user_model().objects.create_user(
            email=payload["email"], password=payload["password"]
        )

        res = self.client.post(
            path=reverse("user:token_obtain_pair"),
            data=payload
        )
        self.refresh = res.data.get("refresh")
        self.access = res.data.get("access")

    def test_register_user(self):
        payload = {"email": "register@test.com", "password": "test_password"}
        url = reverse("user:create")
        res = self.client.post(path=url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data.get("email"),
            get_user_model().objects.last().email
        )

    def test_get_token(self):
        payload = {"email": "test@test.com", "password": "test_password"}
        url = reverse("user:token_obtain_pair")
        res = self.client.post(path=url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", res.data)
        self.assertIn("access", res.data)

    def test_refresh_token(self):
        payload = {"refresh": self.refresh}
        url = reverse("user:token_refresh")
        res = self.client.post(path=url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)

    def test_verify_token(self):
        payload = {"token": self.access}
        url = reverse("user:token_verify")
        res = self.client.post(path=url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_manage_access(self):
        self.client.force_authenticate(self.user)

        res = self.client.get(path=reverse("user:manage"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, res.data.get("email"))
