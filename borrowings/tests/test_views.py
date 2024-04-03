from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from books_service.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer

BORROWING_LIST_URL = reverse("borrowings:borrowings-list")
BORROWING_RETURN_URL = reverse(
    "borrowings:borrowings-return-borrowing", kwargs={"pk": 1}
)


class BorrowingViewTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="email@mail.com",
            password="111222"
        )
        self.book = Book.objects.create(
            title="Big boobs",
            author="Big Bob",
            cover="Hard cover",
            inventory=24,
            daily_fee=100
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today() - timedelta(days=2),
            expected_return_date=date.today() + timedelta(days=5),
            book=self.book,
            user=self.user
        )
        self.client.force_authenticate(self.user)

    def test_return_endpoint_response(self):
        response = self.client.post(BORROWING_RETURN_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_return_borrowing_correct_db_recordings(self):
        response = self.client.post(BORROWING_RETURN_URL)
        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(
            self.borrowing.actual_return_date, date.today()
        )
        self.assertEqual(
            self.book.inventory, 25
        )


class BorrowingViewFilterTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="email@mail.com",
            password="111222",
            is_superuser=False
        )
        self.user2 = get_user_model().objects.create_user(
            email="mail@mail.com",
            password="111222",
            is_superuser=True
        )
        self.book = Book.objects.create(
            title="Big boobs",
            author="Big Bob",
            cover="Hard cover",
            inventory=24,
            daily_fee=100
        )
        self.book2 = Book.objects.create(
            title="Small boobs",
            author="Big Bob",
            cover="Hard cover",
            inventory=24,
            daily_fee=100
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today() - timedelta(days=2),
            expected_return_date=date.today() + timedelta(days=5),
            book=self.book,
            user=self.user
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=date.today() - timedelta(days=2),
            actual_return_date=date.today(),
            expected_return_date=date.today() + timedelta(days=5),
            book=self.book2,
            user=self.user2
        )
        self.client.force_authenticate(self.user)

    def test_is_active_filter(self):
        response = self.client.get(BORROWING_LIST_URL, {"is_active": ""})
        active_borrowings = Borrowing.objects.filter(actual_return_date=None)
        serializer = BorrowingListSerializer(active_borrowings, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_id_filter_non_admin(self):
        response = self.client.get(BORROWING_LIST_URL, {"user_id": "2"})
        borrowing = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingListSerializer(borrowing, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_id_filter_admin(self):
        self.client.force_authenticate(self.user2)

        response = self.client.get(BORROWING_LIST_URL, {"user_id": "2"})
        borrowing = Borrowing.objects.filter(user=self.user2)
        serializer = BorrowingListSerializer(borrowing, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
