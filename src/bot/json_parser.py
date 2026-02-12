import json

from datetime import datetime, timezone

from bot.lexicon import LEXICON, LEXICON_DAYS_RU, LEXICON_PARITY
from core.config import settings, BASE_DIR


def get_today() -> int:
    """Функция, которая определяет сегодняшний день"""

    now = datetime.now(timezone.utc)
    return now.weekday()


def week_parity() -> str:
    """Функция, которая определяет четность недели"""

    today = datetime.now()
    week_number = today.isocalendar().week

    return LEXICON_PARITY[week_number % 2]


def schedule_parser(
    faculty: str,
    current_group: str,
) -> dict:
    """Функция, которая берет из json файла расписание на день"""

    with open(
        f"{BASE_DIR}{settings.schedule.path}{settings.schedule.final_schedule}",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    today_count = get_today()
    today = LEXICON_DAYS_RU[today_count]
    parity = week_parity()

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
) -> str:
    """Функция, которая отправляет готовое расписание на день"""

    today_schedule: dict = schedule_parser(faculty=faculty, current_group=current_group)
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
