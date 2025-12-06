# library_app/views/actions.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from ..forms import DonationBookForm
from ..models import Book, Rental, Donation, Purchase


@login_required
def donate_book(request):
    if request.method == "POST":
        form = DonationBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.donated_by = request.user

            if book.price is not None:
                if book.discount_percent:
                    discount_amount = (book.price * book.discount_percent) / 100
                    book.offer_price = book.price - discount_amount
                else:
                    book.offer_price = book.price
            else:
                book.offer_price = None

            book.available = True
            book.save()

            Donation.objects.create(user=request.user, book=book)
            messages.success(request, f'Thank you for donating "{book.title}".')
        else:
            messages.error(request, "Please correct the errors in the donation form.")
    return redirect("library-home")


@login_required
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        book.available = False
        book.save()
        Rental.objects.create(user=request.user, book=book)
        messages.success(request, f'You rented "{book.title}".')
    else:
        messages.error(request, "This book is not available.")
    return redirect("library-home")


@login_required
def return_book(request, rental_id):
    rental = get_object_or_404(
        Rental, id=rental_id, user=request.user, returned_on__isnull=True
    )
    rental.returned_on = timezone.now()
    rental.save()
    rental.book.available = True
    rental.book.save()
    messages.success(request, f'You returned "{rental.book.title}".')
    return redirect("library-home")


@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Purchase.objects.create(user=request.user, book=book)
    messages.success(request, f'You bought "{book.title}".')
    return redirect("library-home")
