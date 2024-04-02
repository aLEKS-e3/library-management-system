from rest_framework import routers

from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("", BorrowingViewSet, basename="borrowings")


urlpatterns = router.urls

app_name = "borrowings"
