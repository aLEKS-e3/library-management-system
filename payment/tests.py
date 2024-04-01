from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentModelTestCase(TestCase):
    def setUp(self):
        Payment.objects.create(
            status="PAID",
            type="PAYMENT",
            borrowing_id=1,
            session_url="https://example.com",
            session_id="test_session_id",
            money_to_pay=100.00,
        )

    def test_payment_str_representation(self):
        payment = Payment.objects.get(borrowing_id=1)
        self.assertEqual(str(payment), "Paid - Payment - Borrowing ID: 1")


class PaymentSerializerTestCase(TestCase):
    def setUp(self):
        self.payment_data = {
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 2,
            "session_url": "https://test.com",
            "session_id": "test_session_id_2",
            "money_to_pay": 50.00,
        }
        self.serializer = PaymentSerializer(data=self.payment_data)

    def test_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_save(self):
        self.assertTrue(self.serializer.is_valid())
        self.serializer.save()
        payment = Payment.objects.get(borrowing_id=2)
        self.assertEqual(payment.status, "PENDING")


class PaymentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.payment = Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing_id=1,
            session_url="https://example-url.com",
            session_id="test_session_id",
            money_to_pay=100.00,
        )

        self.valid_payload = {
            "status": "PAID",
            "type": "FINE",
            "borrowing_id": 2,
            "session_url": "https://valid-url.com",
            "session_id": "valid_session_id",
            "money_to_pay": 90.00,
        }
        self.invalid_payload = {
            "status": "INVALID",
            "type": "INVALID",
            "borrowing_id": "invalid",
            "session_url": "invalid-url",
            "session_id": "invalid_session_id",
            "money_to_pay": -10.00,
        }

    def test_get_all_payments(self):
        response = self.client.get(reverse("payment-list"))
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_payment(self):
        response = self.client.post(
            reverse("payment-list"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_payment(self):
        response = self.client.post(
            reverse("payment-list"), data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_payment_status(self):
        response = self.client.patch(
            reverse("payment-detail", kwargs={"pk": self.payment.pk}),
            data={"status": "PAID"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
