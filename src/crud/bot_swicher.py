from core import settings


class BotStateService:
    """Управление глобальным состоянием бота через Redis storage"""

    KEY = "bot:is_enabled"

    def __init__(self, redis):
        self.redis = redis

    async def is_enabled(self) -> bool:
        value = await self.redis.get(self.KEY)

        # Если ключа нет, то бот считается включённым
        if value is None:
            return True

        return value == b"1"

    async def enable(self) -> None:
        await self.redis.set(self.KEY, "1")

    async def disable(self) -> None:
        await self.redis.set(self.KEY, "0")
