from telethon.sync import TelegramClient

from .banners import banner, print_successfully, print_telegram_initialization
from .telegram_creds import telegram_api_hash, telegram_api_id, telegram_name

### Banner logo
print(banner)
# Initialize the Telegram client
print_telegram_initialization()

with TelegramClient(telegram_name, telegram_api_id, telegram_api_hash) as client:
    # Authenticate the client
    client.connect()
    print_successfully()
