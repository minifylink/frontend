import asyncio
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
    pass


@dp.message(Command("stat"))
async def cmd_stat(message: types.Message):
    pass


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
