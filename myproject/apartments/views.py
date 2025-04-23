import json
from django.shortcuts import render, get_list_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from data import APARTMENTS

CITIES = [
    "Київ", "Львів", "Одеса", "Харків", "Дніпро",
    "Запоріжжя", "Кривий Ріг", "Миколаїв", "Черкаси"
]


def apartment_detail_view(request, apartment_id):
    # Пошук квартири за id
    user = request.session.get('user')
    print("User from session:", user)

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
    print("User from session:", user)
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
                    "phone": user.get("phone"),
                    "email": user["email"],
                },
                "location": data.get("location")
            }
            APARTMENTS.append(new_apartment)

            return JsonResponse({"status": "ok", "redirect_url": f"/apartments/{new_id}/"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return Http404("Метод не підтримується")

@csrf_exempt
def apartment_edit_view(request, apartment_id):
    # Отримуємо квартиру за id
    apartment = next((apt for apt in APARTMENTS if apt['id'] == apartment_id), None)
    print(apartment)
    if not apartment:
        raise Http404("Квартира не знайдена")

    # Перевірка, чи є користувач власником цієї квартири
    user = request.session.get("user")  # Отримуємо користувача з сесії
    if not user or apartment['owner']['email'] != user.get('email'):
        raise PermissionDenied("У вас немає доступу до редагування цієї квартири")


    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description")
            price = data.get("price")
            location = data.get("location", {})
            city = location.get("city")
            street = location.get("street")
            house_number = location.get("house_number")

            apartment['title'] = title
            apartment['description'] = description
            apartment['price'] = price
            apartment['location'] = {
                'city': city,
                'street': street,
                'house_number': house_number
            }

            print("Apartment after update:", apartment)

            return JsonResponse({"status": "ok", "redirect_url": f"/apartments/{apartment_id}/"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    # Якщо метод GET, повертаємо форму для редагування
    return render(request, 'apartments/add_edit_apartment.html', {
        'apartment': apartment,
        'cities': CITIES,
    })

@csrf_exempt
def apartment_delete_view(request, apartment_id):
    if request.method != "DELETE":
        raise Http404("Метод не підтримується")

    # Знаходимо квартиру
    apartment = next((apt for apt in APARTMENTS if apt['id'] == apartment_id), None)
    if not apartment:
        raise Http404("Квартира не знайдена")

    # Перевірка власника
    user = request.session.get("user")
    if not user or apartment['owner'].get('email') != user.get('email'):
        raise PermissionDenied("Ви не маєте прав на видалення цієї квартири")

    # Видалення
    APARTMENTS.remove(apartment)
    print("Apartment deleted:", apartment)

    response = HttpResponseRedirect("/profile/")
    response.status_code = 303 # це змінює DELETE метод на GET
    return response


def apartments_view(request):
    return render(request, 'apartments/apartments.html', {"apartments": APARTMENTS})