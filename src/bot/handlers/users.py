import logging

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.utils import create_faculties_kb, create_groups_kb
from bot.lexicon.lexicon import LEXICON_INLINE_KEYBOARDS_TYPES
from bot.states import ScheduleStates

users_router = Router()
logger = logging.getLogger(__name__)


@users_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    """Хендлер для команды /start. Отправляет пользователю приветственное сообщение и отображает меню с факультетами."""

    await state.clear()
    await state.set_state(ScheduleStates.choosing_faculty)

    keyboard: InlineKeyboardMarkup = await create_faculties_kb()

    await message.answer(text="Прив", reply_markup=keyboard)
    await message.delete()  # не знаю надо ли удалять, но пусть будет


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

    await callback.message.edit_text(
        text=f"Вы выбрали факультет: {faculty_name}", reply_markup=keyboard
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

    await state.update_data(group=group_name)

    await callback.message.edit_text(text=f"Вы выбрали группу: {group_name}")
    await callback.answer()
