from aiogram.fsm.state import State, StatesGroup


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
    ban_user = State()
    unban_all_users = State()
    write_user = State()
    write_all_users = State()
    stop_bot = State()
    user_list = State()
