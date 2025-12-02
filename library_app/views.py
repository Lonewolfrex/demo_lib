from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, DonationBookForm
from .models import Book, Rental, Donation, Purchase
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator 

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('library-home')
    else:
        form = UserRegisterForm()
    return render(request, 'library_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('library-home')
        else:
            error = "Invalid username or password"
            return render(request, 'library_app/login.html', {'error': error})
    return render(request, 'library_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def library_home(request):
    tab = request.GET.get('tab', 'rent')

    books_qs = Book.objects.all()
    buyable_qs = Book.objects.filter(price__isnull=False)

    # Example pagination: 5 items per page
    page_number = request.GET.get('page', 1)
    if tab == 'rent':
        paginator = Paginator(books_qs, 5)
        books = paginator.get_page(page_number)
        buyable_books = None
    elif tab == 'buy':
        paginator = Paginator(buyable_qs, 5)
        buyable_books = paginator.get_page(page_number)
        books = None
    else:
        books = books_qs
        buyable_books = buyable_qs

    rentals = Rental.objects.filter(user=request.user).order_by('-rented_on')
    donations = Donation.objects.filter(user=request.user).select_related('book').order_by('-donated_on')
    purchases = Purchase.objects.filter(user=request.user).select_related('book').order_by('-purchased_on')

    donation_form = DonationBookForm()

    context = {
        'tab': tab,
        'books': books,
        'buyable_books': buyable_books,
        'rentals': rentals,
        'donations': donations,
        'purchases': purchases,
        'donation_form': donation_form,
    }
    return render(request, 'library_app/home.html', context)


@login_required
def donate_book(request):
    if request.method == 'POST':
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
            messages.error(request, 'Please correct the errors in the donation form.')
    return redirect('library-home')

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Purchase.objects.create(user=request.user, book=book)
    messages.success(request, f'You bought "{book.title}".')
    return redirect('library-home')

@login_required
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        book.available = False
        book.save()
        Rental.objects.create(user=request.user, book=book)
        messages.success(request, f'You rented "{book.title}".')
    else:
        messages.error(request, 'This book is not available.')
    return redirect('library-home')

@login_required
def return_book(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user, returned_on__isnull=True)
    rental.returned_on = timezone.now()
    rental.save()
    rental.book.available = True
    rental.book.save()
    messages.success(request, f'You returned "{rental.book.title}".')
    return redirect('library-home')

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Purchase.objects.create(user=request.user, book=book)
    messages.success(request, f'You bought "{book.title}".')
    return redirect('library-home')