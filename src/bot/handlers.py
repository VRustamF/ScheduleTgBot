import logging

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.json_parser import send_schedule, get_today, week_parity
from bot.utils import create_faculties_kb, create_groups_kb
from bot.lexicon import LEXICON_INLINE_KEYBOARDS_TYPES, LEXICON
from bot.states import ScheduleStates

users_router = Router()
logger = logging.getLogger(__name__)


@users_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    """Хендлер для команды /start. Отправляет пользователю приветственное сообщение и отображает меню с факультетами."""

    await state.clear()
    await state.set_state(ScheduleStates.choosing_faculty)

    keyboard: InlineKeyboardMarkup = await create_faculties_kb()

    await message.answer(text=LEXICON["start"], reply_markup=keyboard)
    await message.delete()


@users_router.callback_query(
    ScheduleStates.choosing_faculty,
    F.data.startswith(f"{LEXICON_INLINE_KEYBOARDS_TYPES["faculties"]}:"),
)
async def process_faculty_selection(callback: CallbackQuery, state: FSMContext):
    """Хендлер для обработки выбора факультета. Отправляет пользователю список групп для выбора."""

    faculty_name = callback.data.split(":")[1]
    logger.info(f"Пользователь выбрал факультет: {faculty_name}")

    await state.update_data(faculty=faculty_name)
    await state.set_state(ScheduleStates.choosing_group)

    keyboard: InlineKeyboardMarkup = await create_groups_kb(faculty=faculty_name)

    message = LEXICON["choice_group"]

    await callback.message.edit_text(
        text=message.format(faculty_name=faculty_name), reply_markup=keyboard
    )
    await callback.answer()


@users_router.callback_query(
    ScheduleStates.choosing_group,
    F.data.startswith(f"{LEXICON_INLINE_KEYBOARDS_TYPES["groups"]}:"),
)
async def process_group_selection(callback: CallbackQuery, state: FSMContext):
    """Хендлер для обработки выбора Группы. Отправляет расписание."""

    group_name = callback.data.split(":")[1]
    logger.info(f"Пользователь выбрал группу: {group_name}")

    data = await state.get_data()

    schedule = send_schedule(faculty=data.get("faculty"), current_group=group_name)
    current_day = get_today()
    parity = "Нечетная" if week_parity().startswith("ч") else "Четная"

    message = LEXICON["schedule_message"]

    await callback.message.edit_text(
        text=message.format(
            group_name=group_name,
            current_week=parity,
            final_schedule=schedule,
            current_day=current_day,
        )
    )
    await callback.answer()
