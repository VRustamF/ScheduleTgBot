from sqlalchemy.ext.asyncio import AsyncSession

from core.db import BotMessage


class BotMessageService:
    """Сервис для crud операций над сообщениями от бота"""

    def __init__(self, session: AsyncSession):
        """Получаем сессию"""
        self.session = session

    async def get_bot_message(self):
        """Функция для получения нужного сообщения"""
        pass

    async def create_bot_message(self):
        """Функция для создания сообщения"""
        pass

    async def update_bot_message(self):
        """Функция для обновления сообщения"""
        pass

    async def delete_bot_message(self):
        """Функция для удаления сообщения"""
        pass
