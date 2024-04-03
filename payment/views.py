import stripe
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing
from payment.models import Payment
from payment.serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_PUBLIC_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id=user.pk)


def create_stripe_session(book):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(book.price * 100),
                    "product_data": {
                        "name": book.title,
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={"book_id": book.id},
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )

    payment = Payment.objects.create(
        book=book,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
    )

    return payment


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get("pk")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return HttpResponseForbidden("Invalid book ID")

        borrowing = Borrowing.objects.create(user=request.user, book=book)
        payment = create_stripe_session(borrowing.book)

        return redirect(payment.session_url)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(borrowings__user=user)
