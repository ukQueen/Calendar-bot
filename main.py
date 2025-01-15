import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from handlers.handlers import router

bot = Bot(token="7610956912:AAFHgZOe23Q-oOIVfSTHHroXY5BT5qaHqUE")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")