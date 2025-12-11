from bots.discord_bot import run_discord_bot
from bots.telegram_bot import run_telegram_bot 
import threading

if __name__ == "__main__":
    
    # Uruchamianie bota Telegrama w osobnym wątku
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.start()
    
    # Uruchamianie bota Discorda w głównym wątku
    run_discord_bot()