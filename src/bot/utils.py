import json

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.inline_kb_builder import create_inline_kb
from core.config import settings, BASE_DIR
from bot.lexicon import LEXICON_INLINE_KEYBOARDS_TYPES, LEXICON_DAYS_RU


async def create_faculties_kb() -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры с факультетами."""

    with open(
        f"{BASE_DIR}{settings.schedule.path}{settings.schedule.final_schedule}",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    faculties = list(data.get("schedules").keys())
    keyboard = create_inline_kb(
        3, LEXICON_INLINE_KEYBOARDS_TYPES["faculties"], *faculties
    )

    return keyboard


async def create_groups_kb(faculty: str) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры с группами."""

    with open(
        f"{BASE_DIR}{settings.schedule.path}{settings.schedule.final_schedule}",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    groups = []
    for group in data.get("schedules").get(faculty):
        groups.append(group.get("group_name"))

    keyboard = create_inline_kb(2, LEXICON_INLINE_KEYBOARDS_TYPES["groups"], *groups)

    return keyboard


async def create_pagination_kb(current_day: int) -> InlineKeyboardMarkup:
    """Функция формирования клавиатуры для пагинации."""

    buttons = {}
    if current_day > 0:
        buttons.update({f"prev:{current_day - 1}": "<<"})  # Кнопка "Назад"

    buttons.update(
        {f"current:{current_day}": f"{LEXICON_DAYS_RU[current_day]}"}
    )  # Кнопка текущего дня для смены четность недели

    if current_day < 6:
        buttons.update({f"next:{current_day + 1}": ">>"})  # Кнопка "Вперед"

    keyboard = create_inline_kb(3, None, **buttons)

    return keyboard
