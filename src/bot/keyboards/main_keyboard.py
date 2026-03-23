from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from bot.lexicon import LEXICON_COMMANDS, LEXICON_ADMIN_COMMANDS


async def set_main_menu(bot: Bot):
    """Формирование меню для обычных пользователей"""

    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS.items()
    ]

    await bot.set_my_commands(
        commands=main_menu_commands, scope=BotCommandScopeDefault()
    )


async def set_admin_main_menu(bot: Bot, admin_id: int):
    """Формирование меню для админа"""

    admin_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_ADMIN_COMMANDS.items()
    ]

    await bot.set_my_commands(
        commands=admin_menu_commands,
        scope=BotCommandScopeChat(chat_id=admin_id),
    )
