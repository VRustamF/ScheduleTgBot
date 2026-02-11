from aiogram.fsm.state import State, StatesGroup


class ScheduleStates(StatesGroup):
    choosing_faculty = State()
    choosing_group = State()
