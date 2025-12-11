import os
from dotenv import load_dotenv
import discord
from discord import app_commands, Intents
from core.logic import create_user_if_not_exists 

# --- KONFIGURACJA / INICJALIZACJA ---
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True 
intents.members = True         
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client) 


# --- KOMENDA /LINK (MODUŁ 1) ---
@tree.command(name="link", description="Generuje kod do połączenia kont Discord i Telegram.")
async def link_command(interaction: discord.Interaction):
    discord_id = interaction.user.id
    username = interaction.user.display_name
    
    link_code, is_new_user = create_user_if_not_exists(discord_id, username)
    
    if is_new_user:
        message = f"✅ Konto utworzone! Kod: **`{link_code}`**."
    else:
        message = f"ℹ️ Jesteś już w systemie! Twój kod: **`{link_code}`**."

    # Wysyłka wiadomości Ephemeral (prywatnej)
    await interaction.response.send_message(message, ephemeral=True)


# --- ZDARZENIA BOTA ---
@client.event
async def on_ready():
    await tree.sync() # Synchronizacja komend
    print(f'Bot Discorda zalogowany jako {client.user} i gotowy.')

# --- FUNKCJA STARTOWA ---
def run_discord_bot():
    if not DISCORD_TOKEN:
        print("Brak klucza DISCORD_TOKEN w .env! Uzupełnij go.")
        return
    client.run(DISCORD_TOKEN)