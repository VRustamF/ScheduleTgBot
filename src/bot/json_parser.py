import json

from datetime import datetime, timezone

from bot.lexicon import LEXICON, LEXICON_DAYS_RU, LEXICON_PARITY
from core.config import settings, BASE_DIR


def get_today() -> int:
    """Функция, которая определяет сегодняшний день"""

    now = datetime.now(timezone.utc)
    return now.weekday()


def week_parity() -> int:
    """Функция, которая определяет четность недели"""

    today = datetime.now()
    week_number = today.isocalendar().week

    return week_number % 2


def schedule_parser(
    faculty: str,
    current_group: str,
    current_day: int | None = None,
    current_parity: int | None = None,
) -> dict:
    """Функция, которая берет из json файла расписание на день"""

    with open(
        f"{BASE_DIR}{settings.schedule.path}{settings.schedule.final_schedule}",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    today_count = get_today() if current_day is None else current_day
    today = LEXICON_DAYS_RU[today_count]

    if current_parity is None:
        parity_count = week_parity()
    else:
        parity_count = week_parity() - 1 if current_parity == 1 else week_parity()
    parity = LEXICON_PARITY[parity_count]

    subjects = {}
    count = 1
    for group in data.get("schedules").get(faculty):
        if group.get("group_name") == current_group:
            for day_schedule in group.get("schedule"):
                if day_schedule.get("day_name") == today:
                    for subject in day_schedule.get("daily_schedule"):
                        time = subject.get("time")
                        subj = subject.get("subject_name")
                        aud = subject.get("audience")

                        if subj.lower()[:2] == parity:
                            continue

                        subjects.update(
                            {
                                count: {
                                    "subj_time": time,
                                    "subj": subj,
                                    "aud": aud,
                                }
                            }
                        )
                        count += 1
    return subjects


def send_schedule(
    faculty: str,
    current_group: str,
    current_day: int | None = None,
    current_parity: int | None = None,
) -> str:
    """Функция, которая отправляет готовое расписание на день"""

    today_schedule: dict = schedule_parser(
        faculty=faculty,
        current_group=current_group,
        current_day=current_day,
        current_parity=current_parity,
    )
    schedule_text = ""

    for i, subject in today_schedule.items():
        schedule_text += (
            LEXICON["schedule"].format(
                i=i,
                time=subject.get("subj_time"),
                subject_name=subject.get("subj"),
                aud=subject.get("aud"),
            )
            + "\n\n"
        )

    return schedule_text
