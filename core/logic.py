import random
import string
from core.database import users_collection 

# --- GENEROWANIE KODU PARUJĄCEGO ---
def generate_link_code(length=6):
    """Generuje unikalny kod (np. E4F7H9) i sprawdza jego unikalność w bazie."""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for i in range(length))
    
    if users_collection.find_one({"link_code": code}):
        return generate_link_code(length)
    return code

# --- TWORZENIE/POBIERANIE UŻYTKOWNIKA ---
def create_user_if_not_exists(discord_id: int, username: str):
    """Tworzy nowy rekord użytkownika Discorda lub zwraca istniejący kod."""
    existing_user = users_collection.find_one({"discord_id": discord_id})
    
    if existing_user:
        return existing_user['link_code'], False 
    
    new_code = generate_link_code()
    new_user_document = {
        "discord_id": discord_id,
        "telegram_id": None,
        "link_code": new_code,
        "username": username
    }
    users_collection.insert_one(new_user_document)
    return new_code, True 

def link_telegram_account(link_code: str, telegram_id: int):
    """Łączy rekord użytkownika z ID Telegrama."""
    user = users_collection.find_one({"link_code": link_code})
    
    if not user or user['telegram_id'] is not None:
        return "not_found" if not user else "already_linked"
        
    users_collection.update_one(
        {"link_code": link_code},
        {"$set": {"telegram_id": telegram_id}}
    )
    return "success"