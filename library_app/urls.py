from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_home, name='library-home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rent/<int:book_id>/', views.rent_book, name='rent-book'),
    path('return/<int:rental_id>/', views.return_book, name='return-book'),
    path('donate/', views.donate_book, name='donate-book'),
    path('buy/<int:book_id>/', views.buy_book, name='buy-book'),
    ]
