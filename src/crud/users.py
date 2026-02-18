from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


from core.db import User


class UserService:
    """Сервис для crud операций над пользователями"""

    def __init__(self, session: AsyncSession):
        """Получаем сессию"""
        self.session = session

    async def get_user(self, user_id: int) -> User | None:
        """Функция для получения пользователя"""

        stmt = select(User).where(User.user_id == user_id)
        user = await self.session.scalar(stmt)

        return user

    async def create_user(
        self,
        user_id: int,
        first_name: str | None,
        username: str | None,
    ) -> User:
        """Функция для создания пользователя"""
        user = User(
            user_id=user_id,
            first_name=first_name,
            username=username,
        )
        self.session.add(user)
        return user

    async def update_user(self, user_id: int, data: dict[str, str]) -> User:
        """Функция для обновления пользователя"""

        stmt = select(User).where(User.user_id == user_id)
        user = await self.session.scalar(stmt)

        for name, value in data.items():
            setattr(user, name, value)

        return user

    async def delete_form_education(self, user_id: int) -> None:
        """Функция для удаления формы обучения у пользователя"""

        stmt = update(User).where(User.user_id == user_id).values(form_education=None)
        await self.session.execute(stmt)

    async def delete_faculty(self, user_id: int) -> None:
        """Функция для удаления факультета у пользователя"""

        stmt = update(User).where(User.user_id == user_id).values(faculty=None)
        await self.session.execute(stmt)

    async def delete_group(self, user_id: int) -> None:
        """Функция для удаления группы у пользователя"""

        stmt = update(User).where(User.user_id == user_id).values(group=None)
        await self.session.execute(stmt)
