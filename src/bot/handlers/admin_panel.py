import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import StateFilter

from bot.filters import is_admin
from bot.keyboards.inline_kb_builder import create_inline_kb
from bot.lexicon import LEXICON_ADMIN_INLINE_KEYBOARD, LEXICON_ADMIN
from bot.states import AdminStates
from schedule_parser import start_schedule_downloader, start_formatter, start_parser

admin_panel_router = Router()

logger = logging.getLogger(__name__)


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

    await callback.message.edit_text(text="Начинаю обновление расписания")

    try:
        logger.info("Начинаем обновление расписания")
        await start_schedule_downloader()
        await start_formatter()
        await start_parser()
        logger.info("Расписание успешно обновлено")

        await callback.message.edit_text(
            text="Расписание обновлено успешно!", reply_markup=keyboard
        )
    except Exception as e:
        logger.exception(f"Ошибка при обновлении расписания: {e}")

        await callback.message.edit_text(
            text="Неизвестная ошибка", reply_markup=keyboard
        )


@admin_panel_router.callback_query(
    is_admin, StateFilter(AdminStates), F.data.startswith("back")
)
async def process_back_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер для кнопки "Назад"."""

    logger.info(f"Админ {callback.from_user.id} выбрал кнопку 'Назад'")

    keyboard: InlineKeyboardMarkup = create_inline_kb(
        1,
        None,
        True,
        **LEXICON_ADMIN_INLINE_KEYBOARD,
    )

    await state.set_state(AdminStates.admin_main_manu)

    await callback.message.edit_text(text=LEXICON_ADMIN["panel"], reply_markup=keyboard)
