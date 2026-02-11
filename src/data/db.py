from pydantic import BaseModel

class Subjects(BaseModel):
    subject_name: str
    audience: str | None
    time: str

class DailySchedules(BaseModel):
    day_name: str
    daily_schedule: list[Subjects] = []

class WeeklySchedules(BaseModel):
    group_name: str
    schedule: list[DailySchedules] = []

class AllSchedules(BaseModel):
    schedules: list[WeeklySchedules] = []


BASE_SCHEDULE = AllSchedules()