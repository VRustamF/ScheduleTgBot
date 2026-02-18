import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.middlewares.db import DatabaseMiddleware
from core import settings, db_helper
from bot.keyboards.main_keyboard import set_main_menu

from bot.handlers import commands_router, schedule_router

logging.basicConfig(
    level=logging.getLevelName(settings.log.level),
    format=settings.log.format,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    storage = MemoryStorage()

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Старт
    @dp.startup()
    async def on_startup():
        await set_main_menu(bot=bot)
        logger.info("Bot started")

    # Остановка — закрываем только то, что aiogram не закрывает сам
    @dp.shutdown()
    async def on_shutdown():
        await db_helper.dispose()
        logger.info("Bot stopped")

    dp.include_router(commands_router)
    dp.include_router(schedule_router)
    dp.update.middleware(DatabaseMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
