from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/literature/", include("books_service.urls", namespace="books_service")),
    path("api/borrowings/", include("borrowings.urls", namespace="borrowings"))
]
