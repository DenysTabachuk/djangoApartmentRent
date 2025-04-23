from django.shortcuts import render, redirect
from data import USERS
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from storage import get_apartments, get_users, add_user, update_apartment, update_user
from django.core.exceptions import PermissionDenied

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

            return redirect("/profile/")
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
        add_user(new_user)
        
        messages.success(request, "Реєстрація успішна. Тепер ви можете увійти.")
        return redirect('/login/')

    return render(request, 'users/register.html')

def profile_view(request):
    user = request.session.get("user")

    if not user:
        return redirect("/login/")

    apartments = get_apartments()
    user_apartments = [apt for apt in apartments if apt['owner']['email'] == user['email']]

    return render(request, 'users/profile.html', {
        "user": user,
        "apartments": user_apartments,
    })

def admin_panel_view(request):
    # Перевірка на статус адміна
    if not request.session.get("user"):
        return redirect("/login/")
    
    if not request.session.get("user").get("is_admin"):
        raise PermissionDenied("У вас немає доступу до адмін панелі")

    users = get_users()
    apartments = get_apartments()
    
    # Розділяємо оголошення на очікуючі та відхилені
    pending_apartments = [apt for apt in apartments if apt["status"] == "pending"]
    rejected_apartments = [apt for apt in apartments if apt["status"] == "rejected"]
    
    # Статистика
    stats = {
        "total_users": len(users),
        "active_users": len([u for u in users if u["is_active"]]),
        "total_apartments": len(apartments),
        "pending_apartments": len(pending_apartments),
        "approved_apartments": len([apt for apt in apartments if apt["status"] == "approved"]),
        "rejected_apartments": len(rejected_apartments),
        "average_price": sum(apt["price"] for apt in apartments) / len(apartments) if apartments else 0,
        "total_owners": len(set(apt["owner"]["email"] for apt in apartments))
    }

    return render(request, "users/admin_panel.html", {
        "users": users,
        "pending_apartments": pending_apartments,
        "rejected_apartments": rejected_apartments,
        "stats": stats
    })

@csrf_exempt
def moderate_apartment_view(request, apartment_id):
    # Перевірка на статус адміна
    if not request.session.get("user") or not request.session.get("user").get("is_admin"):
        raise PermissionDenied("У вас немає доступу до модерації квартир")

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["approved", "rejected"]:
            if update_apartment(apartment_id, {"status": status}):
                messages.success(request, f"Статус квартири успішно змінено на {status}")
            else:
                messages.error(request, "Помилка при оновленні статусу квартири")
    
    return redirect(request.META.get('HTTP_REFERER', '/admin-panel/'))

@csrf_exempt
def logout_view(request):
    request.session.flush()
    return redirect("/login/")

@csrf_exempt
def toggle_user_status_view(request, user_id):
    # Перевірка на статус адміна
    if not request.session.get("user") or not request.session.get("user").get("is_admin"):
        raise PermissionDenied("У вас немає доступу до управління користувачами")

    if request.method == "POST":
        users = get_users()
        user = next((u for u in users if u["id"] == user_id), None)
        
        if user:
            # Змінюємо статус користувача
            user["is_active"] = not user["is_active"]
            # Оновлюємо користувача в базі
            if update_user(user_id, {"is_active": user["is_active"]}):
                messages.success(request, f"Статус користувача успішно змінено")
            else:
                messages.error(request, "Помилка при оновленні статусу користувача")
    
    return redirect(request.META.get('HTTP_REFERER', '/admin-panel/')) 