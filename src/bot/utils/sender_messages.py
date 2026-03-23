import logging

from aiogram import Bot
from aiogram.methods import SendMessage

logger = logging.getLogger(__name__)


async def send_message_to_user(bot: Bot, user_id: int, text: str) -> None:
    """Функция для отправки сообщения другим пользователям"""

    try:
        method = SendMessage(
            chat_id=user_id,
            text=text,
        )

        # Добавляем свой атрибут
        method.skip_single_middleware = True

        await bot(method)
    except Exception as e:
        logger.info(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
