from core.db_deprecated import Subjects, DailySchedules, WeeklySchedules, AllSchedules


def add_subject(
    subject: Subjects,
    base_schedule: AllSchedules,
    group_name: str,
    day_name: str,
    faculty: str,
) -> None:
    """Функция, которая добавляет предмет в дневное расписание группы"""
    for weekly_schedule in base_schedule.schedules[faculty]:
        if group_name == weekly_schedule.group_name:
            for day in weekly_schedule.schedule:
                if day_name == day.day_name:
                    day.daily_schedule.append(subject)
                    return


def add_day(
    base_schedule: AllSchedules,
    day_name: str,
    group_name: str,
    faculty: str,
) -> None:
    """Функция для добавления расписания на день к недельному расписанию группы"""

    for weekly_schedule in base_schedule.schedules[faculty]:
        if group_name == weekly_schedule.group_name:
            weekly_schedule.schedule.append(DailySchedules(day_name=day_name))
            return


def add_schedule(
    base_schedule: AllSchedules,
    schedule: WeeklySchedules,
    faculty: str,
) -> None:
    """Функция для добавления недельного расписания определенного факультета к общему списку расписаний"""

    base_schedule.schedules[faculty].append(schedule)
    return
