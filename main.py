import asyncio
import aiohttp
import logging
import matplotlib.pyplot as plt
from io import BytesIO
from aiogram.types import BufferedInputFile 
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
                'https://шайтанкод.рф/api/v1/shorten',
                json=shorten_data,
                ssl=False
            ) as response:
                if response.status != 200:
                    await message.answer("❌ Ошибка API: что-то не так на стороне сервера :(")
                    return
                
                result = await response.json()
                if result.get("status") != "OK":
                    await message.answer(f"❌ Ошибка API: такая ссылка уже существует!")
                    return
                
                short_url = f"https://шайтанкод.рф/{result['short_id']}"
            
            qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={short_url}"
            
            await message.answer_photo(
                photo=qr_code_url,
                caption=f"✅ Сокращённая ссылка:\n<a href=\"{short_url}\">{short_url}</a>",
                parse_mode="HTML"
            )
    
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")


@dp.message(Command("stat"))
async def cmd_stat(message: types.Message):
    if not message.text or len(message.text.split()) < 2:
        await message.answer("ℹ️ Используйте команду так:\n<code>/stat short_id</code>", parse_mode="HTML")
        return
    
    short_id = message.text.split(maxsplit=1)[1].strip()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://82.202.140.205/api/v1/stats/{short_id}',
                ssl=False
            ) as response:
                if response.status != 200:
                    await message.answer("❌ Ошибка API: что-то не так на стороне сервера :(")
                    return
                
                stats = await response.json()
                clicks = stats.get("clicks", 0)
                devices = stats.get("devices", {})
                countries = stats.get("countries", {})

                report = [
                    f"📊 Статистика для <b>{short_id}</b>",
                    f"👆 Всего переходов: <b>{clicks}</b>"
                ]
                
                if devices:
                    report.append("\n🖥Устройства:");
                    desktop = devices.get("desktop", "0%")
                    mobile = devices.get("mobile", "0%")
                    report.append(f"\tКомпьютеры: {desktop}")
                    report.append(f"\tСмартфоны: {mobile}")
                
                if countries:
                    report.append("\n🌍Страны:")
                    for country in countries:
                        report.append(f"\t{country}")
                
                await message.answer(
                    "\n".join(report),
                    parse_mode="HTML"
                )

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
