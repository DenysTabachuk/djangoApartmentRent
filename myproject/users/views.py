from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, LoginForm
from apartments.models import Apartment
from django.contrib.auth.decorators import login_required

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("profile"))
        else:
            print(form.errors)
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

@login_required(login_url='login') 
def profile_view(request):
    user_apartments = Apartment.objects.filter(owner=request.user)

    return render(request, 'users/profile.html', {
        "user": request.user,
        "apartments": user_apartments,
    })

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect(reverse("login")) 