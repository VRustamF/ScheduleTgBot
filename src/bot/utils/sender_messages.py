import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


async def send_message_to_user(bot: Bot, user_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except Exception as e:
        logger.info(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
