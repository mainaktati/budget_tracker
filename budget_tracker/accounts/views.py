from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from budgets.models import Income, Expense, Budget

def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")
