from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .forms import UserRegistrationForm, LoginForm
from storage import get_apartments

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("profile"))
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("profile"))
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    apartments = get_apartments()
    user_apartments = [apt for apt in apartments if apt['owner']['email'] == request.user.email]

    return render(request, 'users/profile.html', {
        "user": request.user,
        "apartments": user_apartments,
    })

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect(reverse("login")) 