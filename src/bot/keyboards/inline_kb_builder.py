from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.lexicon import LEXICON


def create_inline_kb(
    width: int, button_type: str | None, without_back: bool | None, *args, **kwargs
) -> InlineKeyboardMarkup:
    """Создает клавиатуру на основе переданных аргументов"""

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for btn in args:
            buttons.append(
                InlineKeyboardButton(
                    text=btn,
                    callback_data=f"{button_type}:{btn}" if button_type else btn,
                )
            )

    if kwargs:
        for data, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=data))

    kb_builder.row(*buttons, width=width)

    if not without_back:
        back_button = InlineKeyboardButton(text=LEXICON["back"], callback_data="back")
        kb_builder.row(back_button)

    return kb_builder.as_markup()
