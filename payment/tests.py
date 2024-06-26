from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from books_service.models import Book
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
        }
        self.serializer = PaymentSerializer(data=self.payment_data)

    def test_serializer_not_valid(self):
        self.assertFalse(self.serializer.is_valid())

    def test_serializer_save(self):
        self.payment_data["money_to_pay"] = 50
        self.assertTrue(self.serializer.is_valid())
        self.serializer.save()
        payment = Payment.objects.get(borrowing_id=2)
        self.assertEqual(payment.status, "PENDING")


class PaymentViewSetTestCase(APITestCase):
    PAYMENT_LIST = reverse("payment:payment-list")
    PAYMENT_DETAIL = "payment:payment-detail"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            password="12345",
            email="test@test.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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
        response = self.client.get(self.PAYMENT_LIST)
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_payment(self):
        response = self.client.post(
            self.PAYMENT_LIST, data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_payment(self):
        response = self.client.post(
            self.PAYMENT_LIST, data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_payment_status(self):
        response = self.client.patch(
            reverse(self.PAYMENT_DETAIL, kwargs={"pk": self.payment.pk}),
            data={"status": "PAID"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# class CreateStripeCheckoutSessionViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             password="12345",
#             email="test@test.com",
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         self.book = Book.objects.create(
#             title="Test Book",
#             author="Test Author",
#             daily_fee=10.00,
#             inventory=1,
#         )
#         print(self.book)

    # def test_create_checkout_session(self):
    #     self.client.force_login(self.user)
    #     url = reverse("payment:create-checkout-session")
    #     print(url)
    #     response = self.client.post(url)
    #     print(response.status_code, response.content)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertIn("stripe.com", response.url)
