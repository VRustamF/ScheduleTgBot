import logging

from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserService
from bot.lexicon import (
    LEXICON,
    LEXICON_INLINE_KEYBOARDS_TYPES,
    LEXICON_ADMIN,
    LEXICON_ADMIN_INLINE_KEYBOARD,
)
from bot.utils.keyboard_makers import (
    create_forms_education_kb,
    create_faculties_kb,
    create_groups_kb,
)
from bot.states import ScheduleStates, AdminStates
from bot.utils.sender_messages import send_message_to_user
from bot.keyboards.inline_kb_builder import create_inline_kb
from bot.filters import is_admin

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
            1, LEXICON_INLINE_KEYBOARDS_TYPES["groups"], False, *[user.group]
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

    service = UserService(session=session)
    user_id = message.from_user.id

    keyboard: InlineKeyboardMarkup = await create_forms_education_kb(session=session)

    await service.delete_group(user_id=user_id)
    await service.delete_faculty(user_id=user_id)
    await service.delete_form_education(user_id=user_id)

    await state.set_state(ScheduleStates.choosing_forms_education)

    await message.answer(text=LEXICON["choice_forms_education"], reply_markup=keyboard)


@commands_router.message(is_admin, Command(commands="panel"))
async def process_admin_panel_command(
    message: Message,
    state: FSMContext,
):
    """Хендлер для команды /panel. Отправляет пользователю админ панель."""

    logger.info(f"Админ {message.from_user.id} ввел команду /panel")

    keyboard: InlineKeyboardMarkup = create_inline_kb(
        1,
        None,
        True,
        **LEXICON_ADMIN_INLINE_KEYBOARD,
    )

    await state.set_state(AdminStates.admin_main_manu)

    await message.answer(text=LEXICON_ADMIN["panel"], reply_markup=keyboard)


@commands_router.message(is_admin, Command(commands="ban"))
async def process_ban_user_command(
    message: Message,
    session: AsyncSession,
):
    """Хендлер для бана пользователя"""

    logger.info(f"Админ {message.from_user.id} ввел команду /ban")

    user_id = int(message.text.split(" ")[1])

    service = UserService(session=session)

    user = await service.get_user(user_id=user_id)

    if not user:
        await message.answer(text=LEXICON_ADMIN["not_banned"].format(user_id=user_id))
    else:
        await service.ban_user(user_id=user_id)
        await message.answer(text=LEXICON_ADMIN["banned"].format(user_id=user_id))


@commands_router.message(is_admin, Command(commands="unban"))
async def process_unban_user_command(
    message: Message,
    session: AsyncSession,
):
    """Хендлер для разбана пользователя"""

    logger.info(f"Админ {message.from_user.id} ввел команду /unban")

    user_id = int(message.text.split(" ")[1])

    service = UserService(session=session)

    user = await service.get_user(user_id=user_id)

    if not user:
        await message.answer(text=LEXICON_ADMIN["not_found"].format(user_id=user_id))
    else:
        await service.unban_user(user_id=user_id)
        await message.answer(text=LEXICON_ADMIN["unbanned"].format(user_id=user_id))


@commands_router.message(is_admin, Command(commands="write"))
async def process_write_user_command(
    message: Message,
    session: AsyncSession,
    bot: Bot,
):
    """Хендлер для отправки сообщения пользователю"""

    logger.info(f"Админ {message.from_user.id} ввел команду /write")

    user_id = int(message.text.split(" ")[1].split(":")[0])

    service = UserService(session=session)

    user = await service.get_user(user_id=user_id)

    if not user:
        await message.answer(text=LEXICON_ADMIN["not_found"].format(user_id=user_id))
    else:
        text = message.text.split("::")[1]

        await send_message_to_user(bot=bot, user_id=user_id, text=text)
        await message.answer(text=LEXICON_ADMIN["write"].format(user_id=user_id))


@commands_router.message(is_admin, Command(commands="all"))
async def process_write_all_command(
    message: Message,
    session: AsyncSession,
):
    """Хендлер для отправки сообщения всем пользователям"""

    logger.info(f"Админ {message.from_user.id} ввел команду /all")

    service = UserService(session=session)

    users = await service.get_users()

    if not users:
        await message.answer(text=LEXICON_ADMIN["users_not_found"])
    else:
        text = message.text.split("::")[1]

        await message.answer(
            text=text,
        )
        await message.answer(text=LEXICON_ADMIN["write_all"])


@commands_router.message(is_admin, Command(commands="info"))
async def process_get_user_info_command(
    message: Message,
    session: AsyncSession,
):
    """Хендлер, для получения данных о пользователе"""

    logger.info(f"Админ {message.from_user.id} ввел команду /info")

    servicer = UserService(session=session)

    user_id = int(message.text.split(" ")[1])
    user = await servicer.get_user(user_id=user_id)

    if not user:
        await message.answer(text=LEXICON_ADMIN["not_found"].format(user_id=user_id))
    else:
        await message.answer(
            text=LEXICON_ADMIN["user_info"].format(
                username=user.username,
                id=user.user_id,
                form_education=(
                    user.form_education if user.form_education else "Не выбрано"
                ),
                faculty=user.faculty if user.faculty else "Не выбрано",
                group=user.group if user.group else "Не выбрано",
                ban="Забанен" if user.is_baned else "Не забанен",
            )
        )
