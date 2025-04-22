from django.shortcuts import render, redirect
from data import USERS
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from data import APARTMENTS

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(USERS)
        user = next((u for u in USERS if u["email"] == email and u["password"] == password), None)

        if user:
            request.session["user"] = user
            print(request.session.items()) 

            return redirect("/profile/")
        else:
            return render(request, "users/login.html", {
                "error": "Невірний email або пароль.",
                "email": email
            })

    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")

        if any(u["email"] == email for u in USERS):
            messages.error(request, "Користувач з таким email вже існує.")
            return redirect('/register/')
        
        if password != confirm_password:
            messages.error(request, "Паролі не співпадають.")
            return redirect('/register/')

        USERS.append({
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "is_active": True,
            "is_admin": False,
        })
        
        messages.success(request, "Реєстрація успішна. Тепер ви можете увійти.")
        return redirect('/login/')

    return render(request, 'users/register.html')

def profile_view(request):
    user = request.session.get("user")  # Отримуємо дані користувача з сесії

    if not user:
        return redirect("/login/")  # Якщо користувач не залогінений, перенаправляємо на сторінку входу

    print(APARTMENTS)
    apartments = [apt for apt in APARTMENTS if apt['owner']['email'] == user['email']]

    return render(request, 'users/profile.html', {
        "user": user,
        "apartments": apartments,
    })

def admin_panel_view(request):
    # Статистика по користувачах
    total_users = len(USERS)
    active_users = sum(1 for user in USERS if user["is_active"])
    
    # Статистика по квартирах
    total_apartments = len(APARTMENTS)
    pending_apartments = [apt for apt in APARTMENTS if apt.get("status") == "pending"]
    approved_apartments = [apt for apt in APARTMENTS if apt.get("status") == "approved"]
    rejected_apartments = [apt for apt in APARTMENTS if apt.get("status") == "rejected"]

    # Обчислення середньої ціни
    average_price = sum(apt["price"] for apt in approved_apartments) / len(approved_apartments) if approved_apartments else 0

    print(APARTMENTS)
    # Статистичні дані
    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "total_apartments": total_apartments,
        "pending_apartments": len(pending_apartments),
        "approved_apartments": len(approved_apartments),
        "rejected_apartments": len(approved_apartments) - len(pending_apartments),  # Відхилені = затверджені - очікують
        "average_price": round(average_price, 2),
        "total_owners": len(set([apt["owner"]["email"] for apt in approved_apartments])),
    }

    # Список користувачів для управління
    users = USERS

    # Список квартир, що очікують модерації
    pending_apartments = pending_apartments

    # Перевірка на статус адміна
    if not request.session.get("user") or not request.session.get("user").get("is_admin"):
        return redirect("/login/")  # Якщо користувач не адмін, перенаправляємо на сторінку входу

    context = {
        "stats": stats,
        "users": users,
        "pending_apartments": pending_apartments,
    }

    return render(request, 'users/admin_panel.html', context)

def logout_view(request):
    request.session.flush()  # Очищаємо сесію
    return redirect("/login/") 