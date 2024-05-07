from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing
from borrowings.utils import calculate_borrowing_price
from payment.models import Payment
from payment.serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing__user=user)


def create_stripe_session(borrowing: Borrowing):
    print(reverse("borrowings:borrowings-list"))
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": calculate_borrowing_price(borrowing),
                    "product_data": {
                        "name": borrowing.book.title,
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={"borrowing_id": borrowing.id},
        mode="payment",
        success_url="https://settings.PAYMENT_SUCCESS_URL",
        cancel_url="http://127.0.0.1:8000/api/borrowings/",
    )

    payment = Payment.objects.create(
        borrowing=borrowing,
        status="Pending",
        type="Payment",
        money_to_pay=calculate_borrowing_price(borrowing),
        session_url=checkout_session.url,
        session_id=checkout_session.id,
    )
    print(payment.session_url)

    return payment


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        borrowing_id = request.POST.get("pk")

        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)

        payment_total = calculate_borrowing_price(borrowing)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(payment_total * 100),
                        "product_data": {
                            "name": borrowing.book.title,
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"book_id": borrowing.book.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )

        payment = Payment.objects.create(
            book=borrowing.book,
            borrowing_id=borrowing.id,
            status="Pending",
            type="Payment",
            money_to_pay=payment_total,
            session_url=checkout_session.url,
            session_id=checkout_session.id,
        )

        return redirect(payment.session_url)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(borrowings__user=user)
