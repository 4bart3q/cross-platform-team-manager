import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

# --- INICJALIZACJA I ŁADOWANIE ZMIENNYCH ---
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

if not MONGO_URI:
    raise ValueError("Brak klucza MONGO_URI w pliku .env! Uzupełnij go.")

# --- PRÓBA POŁĄCZENIA ---
try:
    client = MongoClient(MONGO_URI)
    db = client['TeamManagerDB'] 
    
    client.admin.command('ping') 
    print("Połączenie z bazą danych MongoDB Atlas udane.")

except Exception as e:
    print(f"Błąd połączenia z MongoDB: {e}")
    raise SystemExit(1) 

# --- REFERENCJE DO KOLEKCJI ---
users_collection: Collection = db['users']
events_collection: Collection = db['events']
tasks_collection: Collection = db['tasks']