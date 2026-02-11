from collections import defaultdict

from pydantic import BaseModel


class Subjects(BaseModel):
    """Модель предмета"""

    subject_name: str
    audience: str | None
    time: str


class DailySchedules(BaseModel):
    """Расписание на день"""

    day_name: str
    daily_schedule: list[Subjects] = []


class WeeklySchedules(BaseModel):
    """Расписание на неделю для группы"""

    group_name: str
    schedule: list[DailySchedules] = []


class AllSchedules(BaseModel):
    """Список всех расписаний в формате: Факультет: Недельные расписания для всех групп факультета"""

    schedules: dict[str, list[WeeklySchedules]] = defaultdict(list)


BASE_SCHEDULE = AllSchedules()
