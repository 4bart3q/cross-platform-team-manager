import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from core.logic import link_telegram_account 

# --- KONFIGURACJA / INICJALIZACJA ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# --- HANDLER KOMENDY /START (Z KODEM) ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Obsługuje komendę /start [link_code] i łączy konto."""
    
    # 1. Sprawdzenie, czy podano kod
    if not context.args:
        await update.message.reply_text(
            "Witaj! Aby połączyć konto, użyj komendy w formacie: /start [KOD_PARUJĄCY].\n"
            "Kod uzyskasz, używając komendy /link na Discordzie."
        )
        return
        
    link_code = context.args[0].upper() # Pobierz kod i ujednolic go
    telegram_id = update.effective_user.id
    
    # 2. Wywołanie logiki łączenia konta
    result = link_telegram_account(link_code, telegram_id)
    
    # 3. Odpowiedź użytkownikowi
    if result == "success":
        await update.message.reply_text(
            f"🎉 Sukces! Twoje konto Telegram zostało pomyślnie połączone z kontem Discord. \n"
            f"Możesz teraz otrzymywać zadania i powiadomienia."
        )
    elif result == "already_linked":
        await update.message.reply_text(
            "ℹ️ Twoje konto Telegram jest już połączone z kontem Discord."
        )
    elif result == "not_found":
        await update.message.reply_text(
            "❌ Błąd: Nie znaleziono użytkownika dla podanego kodu parującego. Sprawdź kod i spróbuj ponownie."
        )

# --- FUNKCJA STARTOWA ---
def run_telegram_bot():
    if not TELEGRAM_TOKEN:
        print("Brak klucza TELEGRAM_TOKEN w .env! Uzupełnij go.")
        return

    # Inicjalizacja i uruchomienie bota
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Dodanie handlera komendy /start
    application.add_handler(CommandHandler("start", start_command))

    print('Bot Telegrama jest uruchamiany...')
    application.run_polling(timeout=10) # Uruchomienie bota