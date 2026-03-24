import asyncio
from config import TelegramConfig
from telegram import Bot


config = TelegramConfig()
token = config.token
chat_id = config.chat_id

message_test = 'Test From My Bot!!🥳'
audio_test = 'Douds_fire_2026_02_06_16_30_14.wav'

async def audio_message(audio):
    bot = Bot(token=token)
    async with bot:
        await bot.send_audio(chat_id=chat_id, audio=audio)

async def group_message(message):
    bot = Bot(token=token)
    async with bot:
        await bot.send_message(chat_id=chat_id, text= message)

async def alert(message):
    bot = Bot(token=token)
    async with bot:
        await bot.send_message(chat_id=chat_id, text= message)

if __name__ == '__main__':
    asyncio.run(group_message(message_test))
    asyncio.run(audio_message(audio_test))