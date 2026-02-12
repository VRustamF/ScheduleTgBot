import logging

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.json_parser import send_schedule, get_today, week_parity
from bot.utils import create_faculties_kb, create_groups_kb, create_pagination_kb
from bot.lexicon import (
    LEXICON_INLINE_KEYBOARDS_TYPES,
    LEXICON,
    LEXICON_DAYS_RU,
    LEXICON_PARITY,
)
from bot.states import ScheduleStates

users_router = Router()
logger = logging.getLogger(__name__)


@users_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    """Хендлер для команды /start. Отправляет пользователю приветственное сообщение и отображает меню с факультетами."""

    data = await state.get_data()
    last_msg_id = data.get("last_bot_message_id")

    # Удаляем предыдущее сообщение бота
    if last_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id, message_id=last_msg_id
            )
        except:
            pass  # если уже удалено или сообщения нет — игнорируем

    await state.clear()
    await state.set_state(ScheduleStates.choosing_faculty)

    keyboard: InlineKeyboardMarkup = await create_faculties_kb()

    sent_message = await message.answer(text=LEXICON["start"], reply_markup=keyboard)
    await state.update_data(last_bot_message_id=sent_message.message_id)
    await message.delete()


@users_router.message(Command(commands="help"))
async def process_start_command(message: Message, state: FSMContext):
    """Хендлер для команды /help"""

    data = await state.get_data()
    last_msg_id = data.get("last_bot_message_id")

    # Удаляем предыдущее сообщение бота
    if last_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id, message_id=last_msg_id
            )
        except:
            pass  # если уже удалено или сообщения нет — игнорируем

    sent_message = await message.answer(text=LEXICON["help"])
    await state.update_data(last_bot_message_id=sent_message.message_id)
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

    sent_message = await callback.message.edit_text(
        text=message.format(faculty_name=faculty_name), reply_markup=keyboard
    )
    await state.update_data(last_bot_message_id=sent_message.message_id)
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

    data = await state.get_data()

    schedule = send_schedule(
        faculty=data.get("faculty"), current_group=data.get("group")
    )

    today_count = get_today()
    today = LEXICON_DAYS_RU[today_count]

    parity_count = week_parity()
    parity = "Нечетная" if LEXICON_PARITY[parity_count].startswith("ч") else "Четная"

    message = LEXICON["schedule_message"]
    keyboard: InlineKeyboardMarkup = await create_pagination_kb(current_day=today_count)

    await state.update_data(current_parity=parity_count)
    sent_message = await callback.message.edit_text(
        text=message.format(
            group_name=group_name,
            current_week=parity,
            final_schedule=schedule,
            current_day=today,
        ),
        reply_markup=keyboard,
    )
    await state.update_data(last_bot_message_id=sent_message.message_id)
    await callback.answer()


@users_router.callback_query(F.data.startswith("prev:") | F.data.startswith("next:"))
async def process_pagination(callback: CallbackQuery, state: FSMContext):
    """Хендлер для обработки пагинации. Отправляет расписание на другой день."""

    current_day = int(callback.data.split(":")[1])
    logger.info(f"Пользователь выбрал день: {LEXICON_DAYS_RU[current_day]}")

    data = await state.get_data()
    parity_count = data.get("current_parity")

    schedule = send_schedule(
        faculty=data.get("faculty"),
        current_group=data.get("group"),
        current_day=current_day,
    )

    parity = "Нечетная" if LEXICON_PARITY[parity_count].startswith("ч") else "Четная"

    message = LEXICON["schedule_message"]

    keyboard: InlineKeyboardMarkup = await create_pagination_kb(current_day=current_day)

    sent_message = await callback.message.edit_text(
        text=message.format(
            group_name=data.get("group"),
            current_week=parity,
            final_schedule=schedule,
            current_day=LEXICON_DAYS_RU[current_day],
        ),
        reply_markup=keyboard,
    )
    await state.update_data(last_bot_message_id=sent_message.message_id)
    await callback.answer()


@users_router.callback_query(F.data.startswith("current:"))
async def process_current_day(callback: CallbackQuery, state: FSMContext):
    """Хендлер отправки расписания для того же дня следующей по четности недели."""

    current_day = int(callback.data.split(":")[1])
    logger.info(
        f"Пользователь выбрал кнопку смены чётности недели: {LEXICON_DAYS_RU[current_day]}"
    )

    data = await state.get_data()
    parity_count = data.get("current_parity")

    schedule = send_schedule(
        faculty=data.get("faculty"),
        current_group=data.get("group"),
        current_day=current_day,
        current_parity=parity_count,
    )

    parity = (
        "Нечетная" if not LEXICON_PARITY[parity_count].startswith("ч") else "Четная"
    )

    message = LEXICON["schedule_message"]

    keyboard: InlineKeyboardMarkup = await create_pagination_kb(current_day=current_day)

    await state.update_data(current_parity=0 if parity_count == 1 else 1)
    sent_message = await callback.message.edit_text(
        text=message.format(
            group_name=data.get("group"),
            current_week=parity,
            final_schedule=schedule,
            current_day=LEXICON_DAYS_RU[current_day],
        ),
        reply_markup=keyboard,
    )
    await state.update_data(last_bot_message_id=sent_message.message_id)
    await callback.answer()


@users_router.message()
async def process_start_command(message: Message):
    """Хендлер для сообщений пользователя, которые не являются командами"""

    await message.delete()
