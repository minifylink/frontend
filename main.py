import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from tg_api_key import TG_API_KEY


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_API_KEY)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    msg = """
<b>🌟 MinifyLink 🌟</b>

Я - умный бот, созданный чтобы помогать вам.

📌 Вот что я умею:
- Сокращать ссылки, а также генерировать QR коды к ним
- Предоставлять статистку по сокращенным ссылкам

Нажмите /help чтобы увидеть все возможности!

<code>Жду ваших команд!</code>
"""
    await message.answer(msg, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
