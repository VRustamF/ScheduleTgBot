from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class ZgySiteConfig(BaseModel):
    """Ссылка на расписание. В будущем можно будет добавить ссылки на другие расписания"""

    url: str


class ScheduleFileConfig(BaseModel):
    """Настройки файлов с расписанием"""

    file_name: str = "schedule.xls"  #
    path: str = "/files/"  # Путь к файлам расписания
    final_schedule: str = "schedule.json"  # Финальный файл расписания


class LoggerConfig(BaseModel):
    """Настройки логирования"""

    level: str
    format: str


class BotConfig(BaseModel):
    """Настройки телеграм бота"""

    token: str


class RedisConfig(BaseModel):
    """Настройки редиса"""

    url: str


class Settings(BaseSettings):
    """Основной класс с настройками всего приложения"""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    zgy: ZgySiteConfig
    log: LoggerConfig
    bot: BotConfig
    redis: RedisConfig
    schedule: ScheduleFileConfig = ScheduleFileConfig()


settings = Settings()
