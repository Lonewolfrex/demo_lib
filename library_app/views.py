from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm
from .models import Book, Rental, Donation
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
    books = Book.objects.all()
    return render(request, 'library_app/home.html', {'books': books})

@login_required
def rent_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.available:
        book.available = False
        book.save()
        Rental.objects.create(user=request.user, book=book)
    return redirect('library-home')

@login_required
def return_book(request, rental_id):
    rental = Rental.objects.get(id=rental_id, user=request.user)
    rental.returned_on = timezone.now()
    rental.save()
    rental.book.available = True
    rental.book.save()
    return redirect('library-home')

@login_required
def donate_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title and author:
            Donation.objects.create(user=request.user, book_title=title, author=author)
    return redirect('library-home')
