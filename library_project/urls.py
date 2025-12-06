from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from library_app.api import (
    BookViewSet,
    RentalViewSet,
    DonationViewSet,
    PurchaseViewSet,
    MeView,
    RegisterApiView,
)

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"rentals", RentalViewSet, basename="rental")
router.register(r"donations", DonationViewSet, basename="donation")
router.register(r"purchases", PurchaseViewSet, basename="purchase")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("library_app.urls")),  # existing HTML routes

    path("api-auth/", include("rest_framework.urls")),  # browsable API login/logout
    path("api/", include(router.urls)),                 # /api/books/, /api/rentals/, etc.
    path("api/users/me/", MeView.as_view(), name="users-me"),
    path("api/auth/register/", RegisterApiView.as_view(), name="api-register"),

]
