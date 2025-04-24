from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from apartments.models import Apartment
from django.db.models import Avg

User = get_user_model()

def admin_panel_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    if not request.user.is_staff:
        raise PermissionDenied("У вас немає доступу до адмін панелі")

    users = User.objects.all()
    apartments = Apartment.objects.all()

    pending_apartments = apartments.filter(status="pending")
    rejected_apartments = apartments.filter(status="rejected")

    # Статистика
    stats = {
        "total_users": users.count(),
        "active_users": users.filter(is_active=True).count(),
        "total_apartments": apartments.count(),
        "pending_apartments": pending_apartments.count(),
        "approved_apartments": apartments.filter(status="approved").count(),
        "rejected_apartments": rejected_apartments.count(),
        "average_price": apartments.aggregate(Avg("price"))["price__avg"] or 0,
        "total_owners": User.objects.filter(apartment__isnull=False).distinct().count()
    }

    return render(request, "admin_panel/admin_panel.html", {
        "users": users,
        "pending_apartments": pending_apartments,
        "rejected_apartments": rejected_apartments,
        "stats": stats
    })


def admin_users_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if not request.user.is_staff  :
        raise PermissionDenied("У вас немає доступу до управління користувачами")

    users = User.objects.all()
    return render(request, "admin_panel/admin_users.html", {
        "users": users
    })


@csrf_exempt
def moderate_apartment_view(request, apartment_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    if not request.user.is_staff:
        raise PermissionDenied("У вас немає доступу до модерації квартир")

    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ['approved', 'rejected', 'pending']:
            apartment.status = status
            apartment.save()
        return redirect(reverse("admin_panel"))

    return render(request, "admin_panel/moderate_apartment.html", {
        "apartment": apartment
    })


@csrf_exempt
def toggle_user_status_view(request, user_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    if not request.user.is_staff:
        raise PermissionDenied("У вас немає доступу до управління користувачами")

    if request.user.id == user_id:
        messages.error(request, "Ви не можете заблокувати самого себе")
        return redirect(reverse("admin_panel"))

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    return redirect(reverse("admin_panel"))
