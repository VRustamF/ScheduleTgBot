import aiohttp
import logging

from core import settings, BASE_DIR

logger = logging.getLogger(__name__)

URL = settings.zgy.url


async def schedule_downloader() -> None:
    """Функция, которая парсит расписание по чанкам с сайта згу"""

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        async with session.get(URL) as response:
            response.raise_for_status()

            with open(
                f"{BASE_DIR}{settings.schedule.path}{settings.schedule.file_name}", "wb"
            ) as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                logger.info(f"Файл {settings.schedule.file_name} установлен.")
