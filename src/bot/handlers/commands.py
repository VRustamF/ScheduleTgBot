import logging

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserService
from bot.lexicon import LEXICON, LEXICON_INLINE_KEYBOARDS_TYPES
from bot.utils.keyboard_makers import (
    create_forms_education_kb,
    create_faculties_kb,
    create_groups_kb,
)
from bot.states import ScheduleStates
from bot.keyboards.inline_kb_builder import create_inline_kb

commands_router = Router()

logger = logging.getLogger(__name__)


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    """Хендлер для команды /start. Отправляет пользователю приветственное сообщение и отображает нужное меню."""

    logger.info(f"Пользователь {message.from_user.id} ввёл команду /start")

    service = UserService(session=session)

    user = await service.get_user(user_id=message.from_user.id)

    if not user:
        logger.info(f"Пользователь {message.from_user.id} не найден")

        user = await service.create_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
        )

        logger.info(f"Пользователь {message.from_user.id} создан")

    if user.group:
        keyboard: InlineKeyboardMarkup = create_inline_kb(
            1, LEXICON_INLINE_KEYBOARDS_TYPES["groups"], *[user.group]
        )
        msg = "свою группу"
        await state.set_state(ScheduleStates.choosing_group)
    elif user.faculty:
        keyboard: InlineKeyboardMarkup = await create_groups_kb(
            form_education=str(user.form_education),
            faculty=str(user.faculty),
            session=session,
        )
        msg = "свою группу"
        await state.set_state(ScheduleStates.choosing_group)
    elif user.form_education:
        keyboard: InlineKeyboardMarkup = await create_faculties_kb(
            form_education=str(user.form_education),
            session=session,
        )
        msg = "свой факультет"
        await state.set_state(ScheduleStates.choosing_faculty)
    else:
        keyboard: InlineKeyboardMarkup = await create_forms_education_kb(
            session=session
        )
        msg = "свою форму обучения"
        await state.set_state(ScheduleStates.choosing_forms_education)

    await message.answer(text=LEXICON["start"].format(msg=msg), reply_markup=keyboard)


@commands_router.message(Command(commands="change"))
async def process_change_command(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    """Хендлер для команды /change. Отправляет пользователю меню с факультетами."""

    logger.info(f"Пользователь {message.from_user.id} ввёл команду /change")

    keyboard: InlineKeyboardMarkup = await create_forms_education_kb(session=session)
    msg = "свою форму обучения"
    await state.set_state(ScheduleStates.choosing_forms_education)

    await message.answer(text=LEXICON["choice_forms_education"], reply_markup=keyboard)
