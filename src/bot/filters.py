from aiogram.types import Message, CallbackQuery

from core import settings


async def is_admin(message: Message | CallbackQuery) -> bool:
    """Фильтр, который проверяет, является ли пользователь админом"""

    return message.from_user.id in settings.admins_panel.admins
