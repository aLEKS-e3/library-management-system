from datetime import date

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing
from borrowings.support_functions import calculate_fine
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

    # @action(detail=False, methods=["get"])
    # def success(self, request):
    #     session_id = request.GET.get("session_id")
    #
    #     try:
    #         payment = Payment.objects.get(session_id=session_id)
    #     except Payment.DoesNotExist:
    #         return Response({"error": "Invalid session ID"}, status=400)
    #
    #     stripe_session = stripe.checkout.Session.retrieve(session_id)
    #     if stripe_session.payment_status == "paid":
    #         payment.is_paid = True
    #         payment.save()
    #         return Response({"message": "Payment is successful"}, status=200)
    #     else:
    #         return Response({"error": "Payment failed"}, status=400)
    #
    # @action(detail=False, methods=["get"])
    # def cancel(self, request):
    #     return Response({"message": "Payment canceled"}, status=200)


# def create_stripe_session(borrowing):
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         line_items=[
#             {
#                 "price_data": {
#                     "currency": "usd",
#                     "unit_amount": int(borrowing.book.daily_fee * 100),
#                     "product_data": {
#                         "name": borrowing.book.title,
#                     },
#                 },
#                 "quantity": 1,
#             }
#         ],
#         metadata={"book_id": borrowing.book.id},
#         mode="payment",
#         success_url=settings.PAYMENT_SUCCESS_URL,
#         cancel_url=settings.PAYMENT_CANCEL_URL,
#     )
#
#     payment = Payment.objects.create(
#         book=borrowing.book,
#         borrowing_id=borrowing.id,
#         status="Pending",
#         type="Payment",
#         money_to_pay=checkout_session.amount_total,
#         session_url=checkout_session.url,
#         session_id=checkout_session.id,
#     )
#
#     return payment


def calculate_borrowing_price(borrowing):
    payment = (
        date(borrowing.expected_return_date - borrowing.borrow_date).day
        * borrowing.book.daily_fee
    )
    fine = calculate_fine(borrowing)
    if fine:
        return fine
    return payment


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        borrowing_id = request.POST.get("pk")

        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)

        payment = calculate_borrowing_price(borrowing)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(payment * 100),
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
            money_to_pay=payment,
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


class SuccessPayment(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")

        payment = get_object_or_404(Book, session_id=session_id)

        if payment:
            stripe_session = stripe.checkout.Session.retrieve(session_id)
            if stripe_session.payment_status == "paid":
                payment.is_paid = True
                payment.save()

        return HttpResponse(reverse("payment:success"))


class CancelPayment(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Payment is failed. Please try again")
