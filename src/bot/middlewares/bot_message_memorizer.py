from aiogram import BaseMiddleware
from aiogram.client.session.middlewares.base import BaseRequestMiddleware
from aiogram.methods import SendMessage
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message


class UserMessageDeleterMiddleware(BaseMiddleware):
    """Мидлварь для удаления сообщений пользователя после обработки"""

    async def __call__(self, handler, event: Message, data):

        result = await handler(event, data)

        try:
            await event.delete()
        except:
            pass

        return result


class SingleMessageMiddleware(BaseRequestMiddleware):
    """Мидлварь для запоминания последнего сообщения бота и его удаления при отправке нового"""

    def __init__(self, storage):
        self.storage = storage

    async def __call__(self, make_request, bot, method):

        # Только если создаётся новое сообщение
        if isinstance(method, SendMessage):

            key = StorageKey(
                bot_id=bot.id,
                chat_id=method.chat_id,
                user_id=method.chat_id,
            )

            data = await self.storage.get_data(key)
            last_message_id = data.get("last_bot_message_id")

            if last_message_id:
                try:
                    await bot.delete_message(
                        chat_id=method.chat_id, message_id=last_message_id
                    )
                except:
                    pass

        response = await make_request(bot, method)

        # После отправки сохраняем новый ID
        if isinstance(method, SendMessage):
            key = StorageKey(
                bot_id=bot.id,
                chat_id=method.chat_id,
                user_id=method.chat_id,
            )

            await self.storage.update_data(
                key, {"last_bot_message_id": response.message_id}
            )

        return response
