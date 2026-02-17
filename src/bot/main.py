import sys
import asyncio
import logging
import signal
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from core import settings, db_helper
from bot.keyboards.main_keyboard import set_main_menu

from bot.handlers import users_router

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

    shutdown_event = asyncio.Event()

    def _signal_handler(sig, frame=None):
        logger.info(f"Received signal {sig}, shutting down...")
        shutdown_event.set()

    if sys.platform == "win32":
        # Для windows
        signal.signal(signal.SIGTERM, _signal_handler)
        signal.signal(signal.SIGINT, _signal_handler)
    else:
        # Для unix
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, _signal_handler)

    logger.info("Starting bot...")

    await set_main_menu(bot=bot)
    dp.include_router(users_router)
    await bot.delete_webhook(drop_pending_updates=True)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    logger.info("Bot started")

    await shutdown_event.wait()

    await dp.stop_polling()

    with contextlib.suppress(asyncio.CancelledError):
        await polling_task

    # Закрываем соединения при завершении
    await dp.storage.close()
    await db_helper.dispose()
    await bot.session.close()
    logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
