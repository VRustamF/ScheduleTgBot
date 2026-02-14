import asyncio
import aiofiles
import aiohttp
import logging
from pathlib import Path

from core import settings, BASE_DIR

logger = logging.getLogger(__name__)

URLS = settings.zgy.urls


async def download_schedule(session: aiohttp.ClientSession, key: str, url: str) -> None:
    """Функция, которая качает файл с сайта и записывает его в нужную папку"""

    async with session.get(url) as response:
        response.raise_for_status()
        schedule_path = settings.schedule.path.format(schedule_dir=key)
        file_path = Path(f"{BASE_DIR}/{schedule_path}/{settings.schedule.file_name}")

        # Создать папку если её нет
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, "wb") as f:
            async for chunk in response.content.iter_chunked(8192):
                await f.write(chunk)

        logger.info(f"Файл {settings.schedule.file_name} установлен.")


async def schedule_downloader() -> None:
    """Параллельный парсинг расписания для всех форм обучения"""

    timeout = aiohttp.ClientTimeout(total=300)  # таймаут 5 минут

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        timeout=timeout,
    ) as session:

        tasks = [
            download_schedule(session=session, key=key, url=url)
            for key, url in URLS.items()
        ]

        # return_exceptions=True: если одна задача упадет, то остальные выполнятся
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for key, result in zip(URLS.keys(), results):
            if isinstance(result, Exception):
                logger.error(f"Задача для {key} завершилась с ошибкой: {result}")
