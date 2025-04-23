import json
import os

# Шлях до файлу з даними
DATA_FILE = 'data.json'
USERS_FILE = 'users.json'

def load_data():
    """Завантажує дані з JSON файлу"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": [], "apartments": []}

def save_data(data):
    """Зберігає дані у JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_users():
    """Повертає список користувачів"""
    data = load_data()
    users = data.get("users", [])
    
    # Додаємо ID для користувачів, якщо його немає
    need_save = False
    for i, user in enumerate(users):
        if "id" not in user:
            user["id"] = i + 1
            need_save = True
    
    # Якщо додавали ID, зберігаємо зміни
    if need_save:
        data["users"] = users
        save_data(data)
    
    return users

def get_apartments():
    """Повертає список квартир"""
    data = load_data()
    return data.get("apartments", [])

def add_user(user):
    """Додає нового користувача"""
    data = load_data()
    data["users"].append(user)
    save_data(data)

def add_apartment(apartment):
    """Додає нову квартиру"""
    data = load_data()
    data["apartments"].append(apartment)
    save_data(data)

def update_apartment(apartment_id, updated_data):
    """Оновлює дані квартири"""
    data = load_data()
    for apartment in data["apartments"]:
        if apartment["id"] == apartment_id:
            apartment.update(updated_data)
            save_data(data)
            return True
    return False

def delete_apartment(apartment_id):
    """Видаляє квартиру"""
    data = load_data()
    data["apartments"] = [apt for apt in data["apartments"] if apt["id"] != apartment_id]
    save_data(data)

def update_user(user_id, data):
    try:
        data_dict = load_data()
        users = data_dict.get("users", [])
        user_index = next((i for i, u in enumerate(users) if u.get("id") == user_id), None)
        
        if user_index is not None:
            # Оновлюємо тільки ті поля, які передані в data
            for key, value in data.items():
                users[user_index][key] = value
            
            # Зберігаємо оновлені дані
            data_dict["users"] = users
            save_data(data_dict)
            return True
        return False
    except Exception as e:
        print(f"Error updating user: {e}")
        return False 