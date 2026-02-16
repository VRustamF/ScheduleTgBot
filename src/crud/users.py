from sqlalchemy.ext.asyncio import AsyncSession

from core.db import User


class UserService:
    """Сервис для crud операций над пользователями"""

    def __init__(self, session: AsyncSession):
        """Получаем сессию"""
        self.session = session

    async def get_user(self):
        """Функция для получения пользователя"""
        pass

    async def create_user(self):
        """Функция для создания пользователя"""
        pass

    async def update_user(self):
        """Функция для обновления пользователя"""
        pass

    async def delete_user(self):
        """Функция для удаления пользователя"""
        pass
