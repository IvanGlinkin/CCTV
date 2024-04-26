from telethon.sync import TelegramClient
from .telegram_creds import telegram_name, telegram_api_id, telegram_api_hash
from .banners import banner, print_telegram_initialization, print_successfully

### Banner logo
print(banner)
# Initialize the Telegram client
print_telegram_initialization()

with TelegramClient(telegram_name, telegram_api_id, telegram_api_hash) as client:
    # Authenticate the client
    client.connect()
    print_successfully()