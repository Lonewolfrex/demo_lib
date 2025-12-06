# library_app/views/auth.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from ..forms import UserRegisterForm


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("library-home")
    else:
        form = UserRegisterForm()
    return render(request, "library_app/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("library-home")
        error = "Invalid username or password"
        return render(request, "library_app/login.html", {"error": error})
    return render(request, "library_app/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
