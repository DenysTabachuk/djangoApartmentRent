from django.shortcuts import render, get_list_or_404
from django.http import Http404

# Фіксований список квартир для демонстрації
APARTMENTS = [
    {
        "id": 1,
        "title": "Квартира в центрі Києва",
        "price": 15000,
        "description": "Світла та простора квартира поруч з метро.",
        "owner": {"first_name": "Олена", "last_name": "Іваненко", "phone": "+380501234567"},
        "location": {"city": "Київ", "street": "Хрещатик", "house_number": 22},
    },
    {
        "id": 2,
        "title": "Затишна квартира на Подолі",
        "price": 12000,
        "description": "Ідеально підходить для молодої пари.",
        "owner": {"first_name": "Андрій", "last_name": "Коваленко", "phone": "+380671112233"},
        "location": {"city": "Київ", "street": "Контрактова площа", "house_number": 5},
    },
]


def apartment_detail_view(request, apartment_id):
    # Пошук квартири за id
    apartment = next((item for item in APARTMENTS if item['id'] == apartment_id), None)
    if not apartment:
        raise Http404("Квартира не знайдена")

    # Власник взятий з даних квартири
    owner = apartment['owner']

    # Оскільки немає бази даних, is_owner завжди False
    is_owner = False

    context = {
        'apartment': apartment,
        'owner': owner,
        'is_owner': is_owner,
    }
    return render(request, 'apartments/apartment_detail.html', context)

# Приклад підключення в urls.py
# from django.urls import path
# from .views import apartment_detail_view
# urlpatterns = [
#     path('<int:apartment_id>/', apartment_detail_view, name='apartment_detail'),
# ]
