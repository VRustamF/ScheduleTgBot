import logging
from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import TelegramObject, Message, CallbackQuery

from core import db_helper
from crud.users import UserService

logger = logging.getLogger(__name__)


class BanMiddleware(BaseMiddleware):
    """Middleware для блокировки забаненных пользователей"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        telegram_user = data.get("event_from_user", None)

        if not telegram_user:
            return await handler(event, data)

        async with db_helper.session_factory() as session:
            service = UserService(session=session)
            user = await service.get_user(telegram_user.id)

        if user and user.is_baned:

            # Останавливаем дальнейшую обработку
            raise CancelHandler()

        # Иначе продолжаем обработку
        return await handler(event, data)
