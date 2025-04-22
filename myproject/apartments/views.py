import json
from django.shortcuts import render, get_list_or_404, redirect
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from data import APARTMENTS

CITIES = [
    "Київ", "Львів", "Одеса", "Харків", "Дніпро",
    "Запоріжжя", "Кривий Ріг", "Миколаїв", "Черкаси"
]


def apartment_detail_view(request, apartment_id):
    # Пошук квартири за id
    apartment = next((item for item in APARTMENTS if item['id'] == apartment_id), None)
    if not apartment:
        raise Http404("Квартира не знайдена")

    # Власник взятий з даних квартири
    is_owner = False
    owner = apartment['owner']
    if owner["email"] == request.session.get("user", {}).get("email"):
        is_owner = True

    context = {
        'apartment': apartment,
        'owner': owner,
        'is_owner': is_owner,
    }
    return render(request, 'apartments/apartment_detail.html', context)

@csrf_exempt
def apartment_create_view(request):
    user = request.session.get('user')

    if not user:
        messages.error(request, "Ви не залогінені. Будь ласка, увійдіть в систему.")
        return redirect('/login/')

    if request.method == "GET":

        context = {
        'apartment': None,
        'cities': CITIES,
        }

        return render(request, 'apartments/add_edit_apartment.html', context=context)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            new_id = max([a['id'] for a in APARTMENTS]) + 1 if APARTMENTS else 1
            new_apartment = {
                "id": new_id,
                "title": data.get("title"),
                "description": data.get("description"),
                "price": data.get("price"),
                "owner": {
                    "first_name":  user["first_name"],
                    "last_name": user["last_name"],
                    "phone": user.get("phone", ""),
                },
                "location": data.get("location")
            }
            APARTMENTS.append(new_apartment)

            return JsonResponse({"status": "ok", "redirect_url": f"/apartments/{new_id}/"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return Http404("Метод не підтримується")

def apartments_view(request):
    return render(request, 'apartments/apartments.html', {"apartments": APARTMENTS})

def apartment_edit_view(request, apartment_id):
    # Отримуємо квартиру за id
    apartment = next((apt for apt in APARTMENTS if apt['id'] == apartment_id), None)

    if not apartment:
        raise Http404("Квартира не знайдена")

    # Перевірка, чи є користувач власником цієї квартири
    user = request.session.get("user")  # Отримуємо користувача з сесії
    if not user or apartment['owner']['email'] != user.get('email'):
        raise Http404("У вас немає доступу до редагування цієї квартири")

    if request.method == 'POST':
        # Обробка форми
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        city = request.POST.get("city")
        street = request.POST.get("street")
        house_number = request.POST.get("house_number")

        # Оновлення даних квартири
        apartment['title'] = title
        apartment['description'] = description
        apartment['price'] = price
        apartment['location'] = {
            'city': city,
            'street': street,
            'house_number': house_number
        }

        # Повідомлення про успішне оновлення
        messages.success(request, "Квартиру успішно оновлено.")
        return redirect(f"/apartments/{apartment_id}/")

    # Якщо метод GET, повертаємо форму для редагування
    return render(request, 'apartments/add_edit_apartment.html', {
        'apartment': apartment,
    })