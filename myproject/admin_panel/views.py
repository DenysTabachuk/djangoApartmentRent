from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from storage import get_apartments, get_users, update_apartment, update_user

def admin_panel_view(request):
    # Перевірка на статус адміна
    if not request.session.get("user"):
        return redirect(reverse("login"))
    
    if not request.session["user"].get("is_admin"):
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

    return render(request, "admin_panel/admin_panel.html", {
        "users": users,
        "pending_apartments": pending_apartments,
        "rejected_apartments": rejected_apartments,
        "stats": stats
    })

def admin_users_view(request):
    # Перевірка на статус адміна
    if not request.session.get("user"):
        return redirect("/login/")
    
    if not request.session.get("user").get("is_admin"):
        raise PermissionDenied("У вас немає доступу до управління користувачами")

    users = get_users()
    
    return render(request, "admin_panel/admin_users.html", {
        "users": users
    })

@csrf_exempt
def moderate_apartment_view(request, apartment_id):
    # Перевірка на статус адміна
    if not request.session.get("user"):
        return redirect(reverse("login"))
    
    if not request.session["user"].get("is_admin"):
        raise PermissionDenied("У вас немає доступу до модерації квартир")

    apartments = get_apartments()
    apartment = next((apt for apt in apartments if apt["id"] == apartment_id), None)
    
    if not apartment:
        return redirect(reverse("admin_panel"))
    
    if request.method == "POST":
        status = request.POST.get("status")
        update_apartment(apartment_id, {"status": status})
        return redirect(reverse("admin_panel"))
    
    return render(request, "admin_panel/moderate_apartment.html", {
        "apartment": apartment
    })

@csrf_exempt
def toggle_user_status_view(request, user_id):
    # Перевірка на статус адміна
    if not request.session.get("user"):
        return redirect(reverse("login"))
    
    if not request.session["user"].get("is_admin"):
        raise PermissionDenied("У вас немає доступу до управління користувачами")

    # Перевірка, чи адмін не намагається заблокувати самого себе
    if user_id == request.session["user"]["id"]:
        messages.error(request, "Ви не можете заблокувати самого себе")
        return redirect(reverse("admin_panel"))

    users = get_users()
    user = next((u for u in users if u["id"] == user_id), None)
    
    if not user:
        return redirect(reverse("admin_panel"))
    
    user["is_active"] = not user["is_active"]
    update_user(user_id, {"is_active": user["is_active"]})
    return redirect(reverse("admin_panel"))
