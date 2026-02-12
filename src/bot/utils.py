import json

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.inline_kb_builder import create_inline_kb
from core.config import settings, BASE_DIR
from bot.lexicon import LEXICON_INLINE_KEYBOARDS_TYPES


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
