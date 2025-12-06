# library_app/views/home.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from ..models import Book, Rental, Donation, Purchase
from ..forms import DonationBookForm


@login_required
def library_home(request):
    tab = request.GET.get("tab", "rent")

    books_qs = Book.objects.all().order_by("id")
    buyable_qs = Book.objects.filter(price__isnull=False).order_by("id")
    page_number = request.GET.get("page", 1)

    if tab == "rent":
        paginator = Paginator(books_qs, 5)
        books = paginator.get_page(page_number)
        buyable_books = None
    elif tab == "buy":
        paginator = Paginator(buyable_qs, 5)
        buyable_books = paginator.get_page(page_number)
        books = None
    else:
        books = books_qs
        buyable_books = buyable_qs

    rentals = Rental.objects.filter(user=request.user).order_by("-rented_on")
    donations = (
        Donation.objects.filter(user=request.user)
        .select_related("book")
        .order_by("-donated_on")
    )
    purchases = (
        Purchase.objects.filter(user=request.user)
        .select_related("book")
        .order_by("-purchased_on")
    )

    donation_form = DonationBookForm()

    context = {
        "tab": tab,
        "books": books,
        "buyable_books": buyable_books,
        "rentals": rentals,
        "donations": donations,
        "purchases": purchases,
        "donation_form": donation_form,
    }
    return render(request, "library_app/home.html", context)
