import logging

from core import broker

from schedule_parser import start_schedule_downloader, start_formatter, start_parser

logger = logging.getLogger(__name__)


@broker.task(schedule=[{"cron": "*/45 * * * *"}])
async def schedule_updater() -> None:
    """Функция для обновления расписания в БД"""

    try:
        logger.info("Начинаем обновление расписания")
        await start_schedule_downloader()
        await start_formatter()
        await start_parser()
        logger.info("Расписание успешно обновлено")
    except Exception as e:
        logger.exception(f"Ошибка при обновлении расписания: {e}")
