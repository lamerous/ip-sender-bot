import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def get_public_ip():
    """Функция для получения текущего IP"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org?format=json') as response:
                data = await response.json()
                return data['ip']
    except Exception as e:
        print(f"Ошибка при получении IP: {e}")

@dp.message(Command("ip"))
async def send_ip(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Отправка запроса...")
        current_ip = await get_public_ip()
        await message.answer(f"🌐 Ваш актуальный глобальный IP:\n`{current_ip}`", parse_mode="Markdown")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")