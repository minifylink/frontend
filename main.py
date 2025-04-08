import asyncio
import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from env_data import TG_API_KEY, ADD_LINK, STAT_LINK
from msg_src import START_MSG, HELP_MSG


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_API_KEY)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MSG, parse_mode="HTML")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(HELP_MSG, parse_mode="HTML")


@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(
            "Используйте команду в формате:\n"
            "<code>/add https://example.com short-name</code>",
            parse_mode="HTML"
        )
        return
    
    long_url = parts[1].strip()
    short_id = parts[2].strip()
    
    try:
        async with aiohttp.ClientSession() as session:
            shorten_data = {
                "link": long_url,
                "short_id": short_id
            }
            
            async with session.post(
                'https://82.202.140.205/api/v1/shorten',
                json=shorten_data,
                ssl=False
            ) as response:
                if response.status != 200:
                    await message.answer("❌ Ошибка при сокращении ссылки")
                    return
                
                result = await response.json()
                if result.get("status") != "OK":
                    await message.answer(f"❌ Ошибка API: {result.get('message', 'Unknown error')}")
                    return
                
                short_url = f"https://82.202.140.205/{result['short_id']}"
            
            qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={short_url}"
            
            await message.answer_photo(
                photo=qr_code_url,
                caption=f"✅ Сокращённая ссылка:\n<code>{short_url}</code>",
                parse_mode="HTML"
            )
    
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")


@dp.message(Command("stat"))
async def cmd_stat(message: types.Message):
    pass


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
