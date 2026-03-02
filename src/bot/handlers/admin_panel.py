import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import is_admin
from bot.keyboards.inline_kb_builder import create_inline_kb
from bot.lexicon import LEXICON_ADMIN
from bot.utils.keyboard_makers import create_admin_kb
from bot.states import AdminStates
from crud.bot_swicher import BotStateService
from crud.users import UserService
from schedule_parser import start_schedule_downloader, start_formatter, start_parser

admin_panel_router = Router()

logger = logging.getLogger(__name__)


@admin_panel_router.callback_query(
    is_admin,
    AdminStates.admin_main_manu,
    F.data == "bot_info",
)
async def process_get_bot_info(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot_state_service: BotStateService,
):
    """Хендлер для выдачи технической информации о боте"""

    logger.info(f"Админ {callback.from_user.id} получил справку о боте")

    await state.set_state(AdminStates.bot_info)

    keyboard: InlineKeyboardMarkup = create_inline_kb(1, None, False)

    service = UserService(session)

    bot_state = await bot_state_service.is_enabled()
    users_count = await service.get_users_count()
    banned_count = await service.get_users_count(is_banned=True)

    msg = LEXICON_ADMIN["bot_info"].format(
        bot_state=bot_state,
        update_schedule_time="Неизвестно",  # update_time if update_time else
        users_count=users_count,
        banned_count=banned_count,
    )

    await callback.message.edit_text(text=msg, reply_markup=keyboard)


@admin_panel_router.callback_query(
    is_admin,
    AdminStates.admin_main_manu,
    F.data == "update",
)
async def process_update_schedule(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Хендлер для обновления расписания"""

    await state.set_state(AdminStates.update_schedule)

    keyboard: InlineKeyboardMarkup = create_inline_kb(1, None, False)

    await callback.message.edit_text(text=LEXICON_ADMIN["start_update_schedule"])

    try:
        logger.info("Начинаем обновление расписания")
        await start_schedule_downloader()
        await start_formatter()
        await start_parser()
        logger.info("Расписание успешно обновлено")

        await callback.message.edit_text(
            text=LEXICON_ADMIN["update_successful"], reply_markup=keyboard
        )
    except Exception as e:
        logger.exception(f"Ошибка при обновлении расписания: {e}")

        await callback.message.edit_text(
            text=LEXICON_ADMIN["update_error"], reply_markup=keyboard
        )


@admin_panel_router.callback_query(
    is_admin,
    AdminStates.admin_main_manu,
    F.data == "start_bot",
)
async def process_start_bot(
    callback: CallbackQuery,
    state: FSMContext,
    bot_state_service: BotStateService,
):
    """Хендлер для запуска бота"""

    logger.info(f"Админ {callback.from_user.id} включил бота")

    await state.set_state(AdminStates.enable_bot)

    keyboard: InlineKeyboardMarkup = create_inline_kb(1, None, False)

    await bot_state_service.enable()
    await callback.message.edit_text(
        text=LEXICON_ADMIN["bot_enabled"], reply_markup=keyboard
    )


@admin_panel_router.callback_query(
    is_admin,
    AdminStates.admin_main_manu,
    F.data == "stop_bot",
)
async def process_stop_bot(
    callback: CallbackQuery,
    state: FSMContext,
    bot_state_service: BotStateService,
):
    """Хендлер для остановки бота"""

    logger.info(f"Админ {callback.from_user.id} перевёл бота в сервисный режим")

    await state.set_state(AdminStates.disable_bot)

    keyboard: InlineKeyboardMarkup = create_inline_kb(1, None, False)

    await bot_state_service.disable()
    await callback.message.edit_text(
        text=LEXICON_ADMIN["bot_disabled"], reply_markup=keyboard
    )


@admin_panel_router.callback_query(
    is_admin,
    AdminStates.admin_main_manu,
    F.data == "users_list",
)
async def process_users_list(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Хендлер для отображения списка пользователей"""

    logger.info(f"Админ {callback.from_user.id} выбрал кнопку 'Список пользователей'")

    await state.set_state(AdminStates.user_list)

    keyboard: InlineKeyboardMarkup = create_inline_kb(1, None, False)

    servicer = UserService(session=session)

    users = await servicer.get_users()

    if not users:
        await callback.message.edit_text(
            text=LEXICON_ADMIN["users_not_found"],
            reply_markup=keyboard,
        )
    else:
        text = " ".join(str(user) for user in users)
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
        )


@admin_panel_router.callback_query(
    is_admin, StateFilter(AdminStates), F.data.startswith("back")
)
async def process_back_button(
    callback: CallbackQuery,
    state: FSMContext,
    bot_state_service: BotStateService,
):
    """Хендлер для кнопки "Назад"."""

    logger.info(f"Админ {callback.from_user.id} выбрал кнопку 'Назад'")

    bot_enabled = await bot_state_service.is_enabled()

    keyboard: InlineKeyboardMarkup = await create_admin_kb(bot_enabled=bot_enabled)

    await state.set_state(AdminStates.admin_main_manu)

    await callback.message.edit_text(text=LEXICON_ADMIN["panel"], reply_markup=keyboard)
