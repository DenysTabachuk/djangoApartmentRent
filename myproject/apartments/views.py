import json
from django.shortcuts import render, get_list_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from data import APARTMENTS
from storage import get_apartments, add_apartment, update_apartment, delete_apartment
from django.urls import reverse

CITIES = [
    "Київ", "Львів", "Одеса", "Харків", "Дніпро",
    "Запоріжжя", "Кривий Ріг", "Миколаїв", "Черкаси"
]


def apartment_detail_view(request, apartment_id):
    # Пошук квартири за id
    user = request.session.get('user')
    print("User from session:", user)

    apartment = next((item for item in get_apartments() if item['id'] == apartment_id), None)
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
            apartments = get_apartments()
            new_id = max([a['id'] for a in apartments]) + 1 if apartments else 1
            
            # Визначаємо статус в залежності від того, чи є користувач адміном
            status = "approved" if user.get("is_admin") else "pending"
            
            new_apartment = {
                "id": new_id,
                "title": data.get("title"),
                "description": data.get("description"),
                "price": data.get("price"),
                "owner": {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "phone": user.get("phone"),
                    "email": user["email"],
                },
                "location": data.get("location"),
                "status": status
            }
            add_apartment(new_apartment)

            return JsonResponse({"status": "ok", "redirect_url": f"/apartments/{new_id}/"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return Http404("Метод не підтримується")

@csrf_exempt
def apartment_edit_view(request, apartment_id):
    # Отримуємо квартиру за id
    apartments = get_apartments()
    apartment = next((apt for apt in apartments if apt['id'] == apartment_id), None)
    print(apartment)
    if not apartment:
        raise Http404("Квартира не знайдена")

    # Перевірка, чи є користувач власником цієї квартири
    user = request.session.get("user")
    if not user or apartment['owner']['email'] != user.get('email'):
        raise PermissionDenied("У вас немає доступу до редагування цієї квартири")

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_data = {
                "title": data.get("title"),
                "description": data.get("description"),
                "price": data.get("price"),
                "location": {
                    'city': data.get("location", {}).get("city"),
                    'street': data.get("location", {}).get("street"),
                    'house_number': data.get("location", {}).get("house_number")
                },
                "status": "pending"  
            }
            
            if update_apartment(apartment_id, updated_data):
                return JsonResponse({"status": "ok", "redirect_url": f"/apartments/{apartment_id}/"})
            else:
                return JsonResponse({"error": "Помилка оновлення квартири"}, status=400)

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
    apartments = get_apartments()
    apartment = next((apt for apt in apartments if apt['id'] == apartment_id), None)
    if not apartment:
        raise Http404("Квартира не знайдена")

    # Перевірка власника
    user = request.session.get("user")
    if not user or apartment['owner'].get('email') != user.get('email'):
        raise PermissionDenied("Ви не маєте прав на видалення цієї квартири")

    # Видалення
    delete_apartment(apartment_id)
    print("Apartment deleted:", apartment)

    return redirect(reverse("profile"))


def apartments_view(request):
    apartments = get_apartments()

    apartments = [apt for apt in apartments if apt.get("status") == "approved"]
    
    return render(request, 'apartments/apartments.html', {"apartments": apartments})