from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from crud.schedules import ScheduleService
from bot.lexicon import LEXICON, LEXICON_DAYS_RU, LEXICON_PARITY


def get_today() -> int:
    """Функция, которая определяет сегодняшний день"""

    now = datetime.now()
    return now.weekday() + 1


def week_parity() -> int:
    """Функция, которая определяет четность недели"""

    today = datetime.now()
    week_number = today.isocalendar().week

    return week_number % 2


async def daily_schedule_maker(
    group: str,
    faculty: str,
    form_education: str,
    session: AsyncSession,
    today_count: int | None = None,
    parity_count: int | None = None,
) -> tuple[str | None, int, int]:
    """Функция для получения расписания из БД на день и его форматирования"""

    schedule_service = ScheduleService(session=session)

    schedule = await schedule_service.get_schedule(
        form_education=form_education,
        faculty=faculty,
        group=group,
        with_details=True,
    )

    if not parity_count:
        parity_count = week_parity()
    parity = LEXICON_PARITY[parity_count]

    schedule_text = ""
    for day in schedule.daily_schedules:
        if not today_count:
            today_count = get_today()
        today = LEXICON_DAYS_RU[today_count]
        if day.name == today:
            for subject in day.subjects:
                if parity == subject.parity or not subject.parity:
                    schedule_text += LEXICON["schedule"].format(
                        i=subject.queue_number,
                        time=subject.time,
                        subject_name=subject.name,
                        aud=subject.audience,
                    )
    return schedule_text, today_count, parity_count


async def weekly_schedule_maker(
    group: str,
    faculty: str,
    form_education: str,
    session: AsyncSession,
    parity_count: int | None = None,
) -> tuple[str | None, int]:
    """Функция для получения расписания из БД на неделю и его форматирования"""

    schedule_service = ScheduleService(session=session)

    schedule = await schedule_service.get_schedule(
        form_education=form_education,
        faculty=faculty,
        group=group,
        with_details=True,
    )

    if not parity_count:
        parity_count = week_parity()
    parity = LEXICON_PARITY[parity_count]

    schedule_text = ""
    for day in schedule.daily_schedules:
        day_name = day.name
        daily_schedule_text = ""
        for subject in day.subjects:
            if parity == subject.parity or not subject.parity:
                daily_schedule_text += LEXICON["schedule"].format(
                    i=subject.queue_number,
                    time=subject.time,
                    subject_name=subject.name,
                    aud=subject.audience,
                )
        schedule_text += LEXICON["daily_schedule"].format(
            day=day_name, schedule=daily_schedule_text
        )

    return schedule_text, parity_count
