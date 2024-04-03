from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payment.views import (
    PaymentViewSet,
    CreateStripeCheckoutSessionView,
    SuccessPayment,
    CancelPayment,
)

router = DefaultRouter()
router.register(r"", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowing/create-checkout-session/<int:pk>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "borrowing/create-checkout-session/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("success/", SuccessPayment.as_view(), name="success"),
    path("cancel/", CancelPayment.as_view(), name="cancel"),
]

app_name = "payment"
