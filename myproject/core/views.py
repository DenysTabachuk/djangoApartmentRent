from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'core/home.html')

def custom_error_handler_view(request, exception):
    if isinstance(exception, Http404):
        title = "Сторінку не знайдено"
        message = "Перепрошуємо, але сторінка, яку ви шукаєте, не існує."
    elif isinstance(exception, PermissionDenied):
        title = "Доступ заборонено"
        message = "У вас немає доступу до цієї сторінки."
    else:
        title = "Виникла помилка"
        message = "Щось пішло не так, спробуйте пізніше."

    context = {
        'title': title,
        'message': message
    }

    return render(request, 'core/error.html', context)
