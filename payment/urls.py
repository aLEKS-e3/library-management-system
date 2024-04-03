from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payment.views import PaymentViewSet, CreateStripeCheckoutSessionView

router = DefaultRouter()
router.register(r"", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("api/payment/book/id/create-checkout-session/", CreateStripeCheckoutSessionView.as_view(), name="create-checkout-session"),
]

app_name = "payment"
