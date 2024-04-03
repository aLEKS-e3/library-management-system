from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/literature/", include("books_service.urls", namespace="books_service")),
    path("api/borrowings/", include("borrowings.urls", namespace="borrowings")),
    path("api/payment/", include("payment.urls")),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"),
    path("__debug__/", include("debug_toolbar.urls")),
]
