from storage import get_users, get_apartments, add_user, add_apartment

# Ініціалізація початкових даних, якщо файл порожній
if not get_users():
    initial_admin = {
        "email": "admin@gmail.com",
        "password": "admin123",  
        "first_name": "Admin",
        "last_name": "Adminov",
        "phone": "+380000000000",
        "is_active": True,
        "is_admin": True,
    }
    add_user(initial_admin)

    initial_apartments = [
        {
            "id": 1,
            "title": "Квартира в центрі Києва",
            "price": 15000,
            "description": "Світла та простора квартира поруч з метро.",
            "owner": initial_admin,
            "location": {"city": "Київ", "street": "Хрещатик", "house_number": 22},
            "status": "approved",
        },
        {
            "id": 2,
            "title": "Затишна квартира на Подолі",
            "price": 12000,
            "description": "Ідеально підходить для молодої пари.",
            "owner": initial_admin,
            "location": {"city": "Київ", "street": "Контрактова площа", "house_number": 5},
            "status": "pending",
        },
    ]
    
    for apartment in initial_apartments:
        add_apartment(apartment)

# Експортуємо функції для зручного використання
USERS = get_users
APARTMENTS = get_apartments
