from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'users/login.html')

def register_view(request):
    return render(request, 'users/register.html')

def profile_view(request):
    user = {
        "first_name": "Іван",
        "last_name": "Петренко",
        "phone": "+380501234567",
        "email": "ivan.petrenko@example.com",
        "is_admin": True,  
    }

    apartments = [
        {
            "id": 1,
            "title": "Світла квартира біля парку",
            "price": 10000,
            "location": {
                "city": "Київ",
                "street": "Велика Васильківська",
                "house_number": 15
            },
            "status": "active",
        },
        {
            "id": 2,
            "title": "Затишна студія в центрі",
            "price": 12000,
            "location": {
                "city": "Київ",
                "street": "Хрещатик",
                "house_number": 22
            },
            "status": "pending",
        },
    ]

    return render(request, 'users/profile.html', {
        "user": user,
        "apartments": apartments,
    })


def admin_panel_view(request):
    # Фіксовані статистичні дані
    stats = {
        "total_users": 150,
        "active_users": 120,
        "total_apartments": 75,
        "pending_apartments": 10,
        "approved_apartments": 60,
        "rejected_apartments": 5,
        "average_price": 12500.50,
        "total_owners": 65,
    }

    # Фіксований список користувачів
    users = [
        {"id": 1, "first_name": "Іван", "last_name": "Петренко", "email": "ivan.petrenko@example.com", "phone": "+380501234567", "is_active": True},
        {"id": 2, "first_name": "Олена", "last_name": "Коваль", "email": "olena.koval@example.com", "phone": "+380671234890", "is_active": False},
        {"id": 3, "first_name": "Андрій", "last_name": "Шевченко", "email": "andriy.shev@example.com", "phone": "+380631112233", "is_active": True},
    ]

    # Фіксований список квартир, що очікують модерації
    pending_apartments = [
        {"id": 101, "title": "Квартира біля парку", "owner": {"first_name": "Марія", "last_name": "Іванова"}, "price": 14000},
        {"id": 102, "title": "Студія в центрі", "owner": {"first_name": "Петро", "last_name": "Петренко"}, "price": 11000},
    ]

    context = {
        "stats": stats,
        "users": users,
        "pending_apartments": pending_apartments,
    }

    return render(request, 'users/admin_panel.html', context)
