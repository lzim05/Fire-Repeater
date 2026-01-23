import os
from dotenv import load_dotenv

load_dotenv()

class TelegramConfig:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

#telegram_bot_token = os.getenv(telegram_bot_token)
#telegram_group_id = os.getenv(telegram_group_id)