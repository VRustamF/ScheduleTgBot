from aiogram.fsm.state import State, StatesGroup


class BotStatuses(StatesGroup):
    """Состояния бота"""

    launched = State()
    disabled = State()


class ScheduleStates(StatesGroup):
    """Состояния пользователя"""

    choosing_forms_education = State()
    choosing_faculty = State()
    choosing_group = State()
    read_schedule = State()
    read_weekly_schedule = State()


class AdminStates(StatesGroup):
    """Состояния админа"""

    admin_main_manu = State()
    update_schedule = State()
    user_list = State()
    user_info = State()
