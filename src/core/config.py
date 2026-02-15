from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class ZgySiteConfig(BaseModel):
    """Ссылки на расписания"""

    urls: dict = {
        "ochnoe-bak": "https://norvuz.ru/upload/timetable/1-ochnoe.xls",
        "ochno-zaochnoe-bak": "https://norvuz.ru/upload/timetable/2-ochno-zaochnoe.xls",
        "zaochnoe-bak": "https://norvuz.ru/upload/timetable/3-zaochnoe.xls",
        "ochnoe-mag": "https://norvuz.ru/upload/timetable/4-ochnoe-mag.xls",
        "ochno-zaochnoe-mag": "https://norvuz.ru/upload/timetable/5-ochno-zaochnoe-mag.xls",
        "zaochnoe-mag": "https://norvuz.ru/upload/timetable/6-zaochnoe-mag.xls",
        "ochnoe-asp": "https://norvuz.ru/upload/timetable/7-ochnoe-asp.xls",
    }


class ScheduleFileConfig(BaseModel):
    """Настройки файлов с расписанием"""

    file_name: str = "schedule.xls"  # Название файла базового расписания
    path: str = "/files/{schedule_dir}"  # Путь к файлам расписания
    final_schedule: str = "schedule.json"  # Финальный файл расписания


class LoggerConfig(BaseModel):
    """Настройки логирования"""

    level: str
    format: str


class BotConfig(BaseModel):
    """Настройки телеграм бота"""

    token: str


class DataBaseConfig(BaseModel):
    """Настройки базы данных"""

    url: PostgresDsn


class Settings(BaseSettings):
    """Основной класс с настройками всего приложения"""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    log: LoggerConfig
    bot: BotConfig
    db: DataBaseConfig
    zgy: ZgySiteConfig = ZgySiteConfig()
    schedule: ScheduleFileConfig = ScheduleFileConfig()


settings = Settings()
