from django.urls import path

from borrowings.views import BorrowingListView, BorrowingDetailView


urlpatterns = [
    path(
        "",
        BorrowingListView.as_view(),
        name="borrowing-list"
    ),
    path(
        "<int:pk>/",
        BorrowingDetailView.as_view(),
        name="borrowing-detail"
    )
]

app_name = "borrowings"
