# library_app/urls.py
from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    library_home,
    donate_book,
    rent_book,
    return_book,
    buy_book,
)

urlpatterns = [
    path("", library_home, name="library-home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("donate/", donate_book, name="donate-book"),
    path("rent/<int:book_id>/", rent_book, name="rent-book"),
    path("return/<int:rental_id>/", return_book, name="return-book"),
    path("buy/<int:book_id>/", buy_book, name="buy-book"),
]
