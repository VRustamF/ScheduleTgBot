from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.dispatcher.event.bases import CancelHandler

from core import settings


class BotEnabledMiddleware(BaseMiddleware):
    """Мидлварь, которая отвечает за включение/выключение бота"""

    def __init__(self, bot_state_service):
        self.bot_state_service = bot_state_service

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        telegram_user = data.get("event_from_user")

        if not telegram_user:
            return await handler(event, data)

        user_id = telegram_user.id

        # Если бот включён - продолжаем
        if await self.bot_state_service.is_enabled():
            return await handler(event, data)

        # Админы могут пользоваться
        if user_id in settings.admins_panel.admins:
            return await handler(event, data)

        raise CancelHandler
