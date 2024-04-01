from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
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

        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password"
        )

    def test_password_validation(self):
        payload = {"email": "register@test.com", "password": "shrt"}
        url = reverse("user:create")
        res = self.client.post(path=url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("password"),
            [ErrorDetail(string='Ensure this field has at least 5 characters.', code='min_length')]
        )

    def test_register_user(self):
        payload = {"email": "register@test.com", "password": "test_password"}
        url = reverse("user:create")
        res = self.client.post(path=url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data.get("email"),
            get_user_model().objects.last().email
        )

    def test_user_manage_access(self):
        self.client.force_authenticate(self.user)

        res = self.client.get(path=reverse("user:manage"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, res.data.get("email"))
