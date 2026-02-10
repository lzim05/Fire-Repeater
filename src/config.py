import os
from dotenv import load_dotenv

load_dotenv()

class TelegramConfig:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
