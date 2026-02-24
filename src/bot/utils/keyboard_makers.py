from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from crud.schedules import ScheduleService
from bot.keyboards.inline_kb_builder import create_inline_kb
from bot.lexicon import LEXICON_INLINE_KEYBOARDS_TYPES, LEXICON_DAYS_RU, LEXICON_PARITY


async def create_forms_education_kb(session: AsyncSession) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры с формами обучения"""

    service = ScheduleService(session=session)
    forms_education = await service.get_forms_education()

    keyboard = create_inline_kb(
        1,
        LEXICON_INLINE_KEYBOARDS_TYPES["forms_education"],
        True,
        *forms_education,
    )

    return keyboard


async def create_faculties_kb(
    form_education: str, session: AsyncSession
) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры с факультетами."""

    service = ScheduleService(session=session)
    faculties = await service.get_faculties(form_education=form_education)

    keyboard = create_inline_kb(
        3,
        LEXICON_INLINE_KEYBOARDS_TYPES["faculties"],
        False,
        *faculties,
    )

    return keyboard


async def create_groups_kb(
    form_education: str, faculty: str, session: AsyncSession
) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры с группами."""

    service = ScheduleService(session=session)
    groups = await service.get_groups(form_education=form_education, faculty=faculty)

    keyboard = create_inline_kb(
        2,
        LEXICON_INLINE_KEYBOARDS_TYPES["groups"],
        False,
        *groups,
    )

    return keyboard


async def create_pagination_kb(
    current_day: int, parity_count: int
) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры для пагинации."""

    buttons = {}
    if current_day > 1:
        buttons.update(
            {f"prev:{current_day - 1}:{parity_count}": "<<"}
        )  # Кнопка "Назад"

    buttons.update(
        {f"current:{current_day}:{parity_count}": f"{LEXICON_DAYS_RU[current_day]}"}
    )  # Кнопка текущего дня для смены четность недели

    buttons.update({f"weekly:{parity_count}": "Неделя"})  # Кнопка для просмотра недели

    if current_day < 7:
        buttons.update(
            {f"next:{current_day + 1}:{parity_count}": ">>"}
        )  # Кнопка "Вперед"

    keyboard = create_inline_kb(
        4,
        None,
        False,
        **buttons,
    )

    return keyboard


async def create_weekly_kb(parity_count: int) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры для недельного расписания."""

    buttons = {}

    buttons.update(
        {f"current_week:{parity_count}": "Сменить неделю"}
    )  # Кнопка для смены четность недели

    keyboard = create_inline_kb(
        1,
        None,
        False,
        **buttons,
    )

    return keyboard
