import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from core.config import settings
from bot.keyboards.main_keyboard import set_main_menu

from bot.handlers import users_router

logging.basicConfig(
    level=logging.getLevelName(settings.log.level),
    format=settings.log.format,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    storage = RedisStorage.from_url(settings.redis.url)

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    logger.info("Starting bot...")

    await set_main_menu(bot=bot)

    dp.include_router(users_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
