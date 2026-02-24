from aiogram.fsm.state import State, StatesGroup


class ScheduleStates(StatesGroup):
    choosing_forms_education = State()
    choosing_faculty = State()
    choosing_group = State()
    read_schedule = State()
    read_weekly_schedule = State()
