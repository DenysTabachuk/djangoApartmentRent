import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .models import Apartment
from .forms import ApartmentForm


def apartment_detail_view(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    is_owner = request.user.is_authenticated and apartment.owner == request.user

    context = {
        'apartment': apartment,
        'owner': apartment.owner,
        'is_owner': is_owner,
    }
    return render(request, 'apartments/apartment_detail.html', context)


@csrf_exempt
@login_required
def apartment_edit_create_view(request, apartment_id=None):
    user = request.user

    if apartment_id:  
        apartment = get_object_or_404(Apartment, id=apartment_id)
        if apartment.owner != user:
            raise PermissionDenied("Ви не маєте доступу до редагування цієї квартири")
    else:
        apartment = None

    if request.method == "GET":
        form = ApartmentForm(instance=apartment)  
        context = {'apartment': apartment, 'form': form}
        return render(request, 'apartments/add_edit_apartment.html', context)

    elif request.method == "POST":
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.owner = user  

            if apartment_id and not user.is_staff:
                apartment.status = "pending"
            else:
                if user.is_staff or user.is_superuser:
                    apartment.status = "approved"

            apartment.save()
            return redirect(reverse("profile"))  
        else:
            context = {'apartment': apartment, 'form': form}
            return render(request, 'apartments/add_edit_apartment.html', context)

    return HttpResponseNotAllowed(['GET', 'POST'])


@require_http_methods(["DELETE"])
@login_required
def apartment_delete_view(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if apartment.owner != request.user:
        raise PermissionDenied("Ви не маєте прав на видалення цієї квартири")

    apartment.delete()
    print("Apartment deleted:", apartment)

    return redirect(reverse("profile"))


def apartments_view(request):
    city = request.GET.get('city')
    sort = request.GET.get('sort')

    apartments = Apartment.objects.filter(status='approved')

    if city:
        apartments = apartments.filter(location__city=city)

    if sort == 'price_asc':
        apartments = apartments.order_by('price')
    elif sort == 'price_desc':
        apartments = apartments.order_by('-price')

    context = {
        "apartments": apartments,
        "selected_city": city,
        "selected_sort": sort,
        "apartment_model": Apartment  # Для доступу до CITY_CHOICES
    }
    return render(request, 'apartments/apartments.html', context)
