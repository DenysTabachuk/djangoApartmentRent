from django.shortcuts import render, redirect
from data import USERS
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from storage import get_apartments, get_users, add_user
from django.urls import reverse

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        users = get_users()
        user = next((u for u in users if u["email"] == email and u["password"] == password), None)

        if user:
            if not user.get("is_active", True):
                messages.error(request, "Ваш акаунт заблоковано. Зверніться до адміністратора.")
                return render(request, 'users/login.html', {"email": email})
                
            request.session["user"] = user
            print(request.session.items()) 

            return redirect(reverse("profile"))
        else:
            messages.error(request, "Невірний email або пароль.")
            return render(request, 'users/login.html', {"email": email})

    return render(request, 'users/login.html')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")

        users = get_users()
        if any(u["email"] == email for u in users):
            messages.error(request, "Користувач з таким email вже існує.")
            return render(request, 'users/register.html', {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone
            })
        
        if password != confirm_password:
            messages.error(request, "Паролі не співпадають.")
            return render(request, 'users/register.html', {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone
            })

        # Генеруємо новий ID
        new_id = max([u.get("id", 0) for u in users]) + 1 if users else 1

        new_user = {
            "id": new_id,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "is_active": True,
            "is_admin": False,
        }
        if add_user(new_user):
            request.session["user"] = new_user
            return redirect(reverse("profile"))
        else:
            messages.error(request, "Помилка при створенні користувача")
            return render(request, 'users/register.html', {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone
            })

    return render(request, 'users/register.html')

def profile_view(request):
    user = request.session.get("user")

    if not user:
        return redirect(reverse("login"))

    apartments = get_apartments()
    user_apartments = [apt for apt in apartments if apt['owner']['email'] == user['email']]

    return render(request, 'users/profile.html', {
        "user": user,
        "apartments": user_apartments,
    })

@csrf_exempt
def logout_view(request):
    request.session.flush()
    return redirect(reverse("login")) 