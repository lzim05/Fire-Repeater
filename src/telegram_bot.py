import asyncio
from config import TelegramConfig
from telegram import Bot


config = TelegramConfig()
token = config.token
chat_id = config.chat_id

message_test = 'Test From My Bot!!🥳'
audio_test = 'Douds_fire_2026_02_06_16_30_14.wav'

async def group_message(audio,message):
    bot = Bot(token=token)

    async with bot:
        await bot.send_audio(chat_id=chat_id, audio=audio)
        await bot.send_message(chat_id=chat_id, text= message)

async def alert(message):
    bot = Bot(token=token)
    async with bot:
        await bot.send_message(chat_id=chat_id, text= message)

if __name__ == '__main__':
    asyncio.run(group_message(audio_test,message_test))