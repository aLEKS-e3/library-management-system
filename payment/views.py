from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payment.models import Payment
from payment.serializers import PaymentSerializer

import stripe

stripe.api_key = "SECRET_KEY"


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=user)

    @action(detail=True, methods=["get"])
    def success(self, request, pk=None):
        payment = self.get_object()
        payment_id = payment.session_id
        try:
            stripe_payment = stripe.PaymentIntent.retrieve(payment_id)
            if stripe_payment.status == "succeeded":
                payment.status = "PAID"
                payment.save()
                return Response(
                    {"message": "Payment successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST
                )
        except stripe.error.InvalidRequestError:
            return Response(
                {"message": "Invalid payment ID"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"])
    def cancel(self, request):
        return Response({"message": "Payment cancelled"}, status=status.HTTP_200_OK)
