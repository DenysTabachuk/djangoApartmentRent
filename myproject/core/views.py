from django.shortcuts import render

apartments = [
    {
        "id": 1,
        "title": "Квартира в центрі Києва",
        "price": 15000,
        "description": "Світла та простора квартира поруч з метро.",
        "owner": {
            "first_name": "Олена",
            "last_name": "Іваненко",
            "phone": "+380501234567"
        },
        "location": {
            "city": "Київ",
            "street": "Хрещатик",
            "house_number": 22
        }
    },
    {
        "id": 2,
        "title": "Затишна квартира на Подолі",
        "price": 12000,
        "description": "Ідеально підходить для молодої пари.",
        "owner": {
            "first_name": "Андрій",
            "last_name": "Коваленко",
            "phone": "+380671112233"
        },
        "location": {
            "city": "Київ",
            "street": "Контрактова площа",
            "house_number": 5
        }
    }
]

def home(request):
    return render(request, 'core/home.html', {"apartments": apartments})
