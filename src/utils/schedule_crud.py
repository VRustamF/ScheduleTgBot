from data.db import BASE_SCHEDULE, Subjects, DailySchedules, WeeklySchedules

def add_subject(
        subject: Subjects,
        group_name: str,
        day_name: str,
):
    for weekly_schedule in BASE_SCHEDULE.schedules:
        if group_name == weekly_schedule.group_name:
            for day in weekly_schedule.schedule:
                if day_name == day.day_name:
                    day.daily_schedule.append(subject)
                    return


def add_day(
        day_name: str,
        group_name: str,
):
    for weekly_schedule in BASE_SCHEDULE.schedules:
        if group_name == weekly_schedule.group_name:
            weekly_schedule.schedule.append(DailySchedules(day_name=day_name))
            return

def add_schedule(
        schedule: WeeklySchedules,
):
    BASE_SCHEDULE.schedules.append(schedule)
    return