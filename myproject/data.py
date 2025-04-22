USERS = [
    {
        "email": "admin@gmail.com",
        "password": "admin123",  
        "first_name": "Admin",
        "last_name": "Adminov",
        "phone": "+380000000000",
        "is_active": True,
        "is_admin": True,
    },
]

APARTMENTS = [
    {
        "id": 1,
        "title": "Квартира в центрі Києва",
        "price": 15000,
        "description": "Світла та простора квартира поруч з метро.",
        "owner": USERS[0],  # Адмін як власник
        "location": {"city": "Київ", "street": "Хрещатик", "house_number": 22},
        "status": "approved",  # Статус квартири (approved, pending, rejected)
    },
    {
        "id": 2,
        "title": "Затишна квартира на Подолі",
        "price": 12000,
        "description": "Ідеально підходить для молодої пари.",
        "owner": USERS[0],  # Адмін як власник
        "location": {"city": "Київ", "street": "Контрактова площа", "house_number": 5},
        "status": "pending",  # Статус квартири (approved, pending, rejected)
    },
]
