from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/literature/", include("books_service.urls", namespace="books_service"))
]
