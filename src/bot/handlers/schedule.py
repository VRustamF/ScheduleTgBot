import logging

from aiogram import Router, F

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserService
from bot.states import ScheduleStates
from bot.lexicon import (
    LEXICON,
    LEXICON_INLINE_KEYBOARDS_TYPES,
    LEXICON_DAYS_RU,
    LEXICON_PARITY,
)
from bot.utils.schedule_maker import schedule_maker, week_parity
from bot.utils.keyboard_makers import (
    create_faculties_kb,
    create_groups_kb,
    create_pagination_kb,
    create_forms_education_kb,
)

schedule_router = Router()
logger = logging.getLogger(__name__)


@schedule_router.callback_query(
    ScheduleStates.choosing_forms_education,
    F.data.startswith(f"{LEXICON_INLINE_KEYBOARDS_TYPES["forms_education"]}:"),
)
async def process_form_education_selection(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Хендлер для обработки выбора формы обучения. Отправляет пользователю список факультетов для выбора."""

    form_education_name = callback.data.split(":")[1]
    logger.info(
        f"Пользователь {callback.from_user.id} выбрал форму обучения: {form_education_name}"
    )

    service = UserService(session=session)

    await service.update_user(
        user_id=callback.from_user.id, data={"form_education": form_education_name}
    )

    await state.set_state(ScheduleStates.choosing_faculty)

    keyboard: InlineKeyboardMarkup = await create_faculties_kb(
        form_education=str(form_education_name),
        session=session,
    )

    message = LEXICON["choice_faculty"]

    sent_message = await callback.message.edit_text(
        text=message.format(form_education_name=form_education_name),
        reply_markup=keyboard,
    )
    # await state.update_data(last_bot_message_id=sent_message.message_id)
    await callback.answer()


@schedule_router.callback_query(
    ScheduleStates.choosing_faculty,
    F.data.startswith(f"{LEXICON_INLINE_KEYBOARDS_TYPES["faculties"]}:"),
)
async def process_faculty_selection(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Хендлер для обработки выбора факультета. Отправляет пользователю список групп для выбора."""

    faculty_name = callback.data.split(":")[1]
    logger.info(
        f"Пользователь {callback.from_user.id} выбрал факультет: {faculty_name}"
    )

    service = UserService(session=session)

    user = await service.get_user(user_id=callback.from_user.id)

    await service.update_user(
        user_id=callback.from_user.id, data={"faculty": faculty_name}
    )

    await state.set_state(ScheduleStates.choosing_group)

    keyboard: InlineKeyboardMarkup = await create_groups_kb(
        form_education=str(user.form_education),
        faculty=faculty_name,
        session=session,
    )

    message = LEXICON["choice_group"]

    sent_message = await callback.message.edit_text(
        text=message.format(faculty_name=faculty_name), reply_markup=keyboard
    )

    await callback.answer()


@schedule_router.callback_query(
    ScheduleStates.choosing_group,
    F.data.startswith(f"{LEXICON_INLINE_KEYBOARDS_TYPES["groups"]}:"),
)
async def process_group_selection(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Хендлер для обработки выбора Группы. Отправляет расписание."""

    group_name = callback.data.split(":")[1]
    logger.info(f"Пользователь {callback.from_user.id} выбрал группу: {group_name}")

    service = UserService(session=session)

    user = await service.get_user(user_id=callback.from_user.id)

    await service.update_user(user_id=callback.from_user.id, data={"group": group_name})

    await state.set_state(ScheduleStates.read_schedule)

    schedule, today_count, parity_count = await schedule_maker(
        group=group_name,
        faculty=str(user.faculty),
        form_education=str(user.form_education),
        session=session,
    )

    message = LEXICON["schedule_message"]
    keyboard: InlineKeyboardMarkup = await create_pagination_kb(
        current_day=today_count,
        parity_count=parity_count,
    )

    sent_message = await callback.message.edit_text(
        text=message.format(
            group_name=group_name,
            week="Текущая неделя",
            current_week=LEXICON_PARITY[parity_count],
            day=LEXICON_DAYS_RU[today_count],
            final_schedule=schedule if schedule else LEXICON["nothing"],
            current_day=LEXICON_DAYS_RU[today_count],
        ),
        reply_markup=keyboard,
    )
    await callback.answer()


@schedule_router.callback_query(F.data.startswith("prev:") | F.data.startswith("next:"))
async def process_pagination(callback: CallbackQuery, session: AsyncSession):
    """Хендлер для обработки пагинации. Отправляет расписание на другой день."""

    selected_day = int(callback.data.split(":")[1])
    selected_parity = int(callback.data.split(":")[2])
    logger.info(
        f"Пользователь {callback.from_user.id} выбрал день: {LEXICON_DAYS_RU[selected_day]} - {selected_day}"
    )

    service = UserService(session=session)

    user = await service.get_user(user_id=callback.from_user.id)

    schedule, _, parity_count = await schedule_maker(
        group=str(user.group),
        faculty=str(user.faculty),
        form_education=str(user.form_education),
        session=session,
        today_count=selected_day,
        parity_count=selected_parity,
    )

    message = LEXICON["schedule_message"]

    keyboard: InlineKeyboardMarkup = await create_pagination_kb(
        current_day=selected_day,
        parity_count=parity_count,
    )

    week = "Следующая неделя" if parity_count != week_parity() else "Текущая неделя"

    sent_message = await callback.message.edit_text(
        text=message.format(
            group_name=user.group,
            week=week,
            current_week=LEXICON_PARITY[parity_count],
            day=LEXICON_DAYS_RU[selected_day],
            final_schedule=schedule if schedule else LEXICON["nothing"],
            current_day=LEXICON_DAYS_RU[selected_day],
        ),
        reply_markup=keyboard,
    )
    await callback.answer()


@schedule_router.callback_query(F.data.startswith("current:"))
async def process_change_day_parity(callback: CallbackQuery, session: AsyncSession):
    """Хендлер отправки расписания для того же дня следующей по четности недели."""

    selected_day = int(callback.data.split(":")[1])
    selected_parity = int(callback.data.split(":")[2])
    logger.info(
        f"Пользователь {callback.from_user.id} выбрал кнопку смены чётности недели. "
        f"Текущая четность: {LEXICON_PARITY[selected_parity]}."
    )

    service = UserService(session=session)

    user = await service.get_user(user_id=callback.from_user.id)

    parity_count = 1 - selected_parity

    schedule, _, _ = await schedule_maker(
        group=str(user.group),
        faculty=str(user.faculty),
        form_education=str(user.form_education),
        session=session,
        today_count=selected_day,
        parity_count=parity_count,
    )

    message = LEXICON["schedule_message"]

    keyboard: InlineKeyboardMarkup = await create_pagination_kb(
        current_day=selected_day, parity_count=parity_count
    )

    week = "Следующая неделя" if parity_count != week_parity() else "Текущая неделя"

    sent_message = await callback.message.edit_text(
        text=message.format(
            group_name=user.group,
            week=week,
            current_week=LEXICON_PARITY[parity_count],
            day=LEXICON_DAYS_RU[selected_day],
            final_schedule=schedule if schedule else LEXICON["nothing"],
            current_day=LEXICON_DAYS_RU[selected_day],
        ),
        reply_markup=keyboard,
    )
    await callback.answer()


@schedule_router.callback_query(F.data.startswith("back"))
async def process_back_button(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Хендлер для кнопки "Назад". Возвращает пользователя к выбору дня недели."""

    logger.info(f"Пользователь {callback.from_user.id} выбрал кнопку 'Назад'")

    current_state = await state.get_state()

    if current_state == ScheduleStates.read_schedule:
        await state.set_state(ScheduleStates.choosing_group)

        service = UserService(session=session)
        user = await service.get_user(user_id=callback.from_user.id)

        await service.delete_group(user_id=callback.from_user.id)

        keyboard: InlineKeyboardMarkup = await create_groups_kb(
            form_education=str(user.form_education),
            faculty=str(user.faculty),
            session=session,
        )

        message = LEXICON["choice_group"]

        sent_message = await callback.message.edit_text(
            text=message.format(faculty_name=user.faculty),
            reply_markup=keyboard,
        )

    elif current_state == ScheduleStates.choosing_group.state:
        await state.set_state(ScheduleStates.choosing_faculty)

        service = UserService(session=session)
        user = await service.get_user(user_id=callback.from_user.id)

        keyboard: InlineKeyboardMarkup = await create_faculties_kb(
            form_education=str(user.form_education),
            session=session,
        )

        service = UserService(session=session)

        await service.delete_faculty(user_id=callback.from_user.id)

        message = LEXICON["choice_faculty"]

        sent_message = await callback.message.edit_text(
            text=message.format(form_education_name=user.form_education),
            reply_markup=keyboard,
        )

    elif current_state == ScheduleStates.choosing_faculty:
        await state.set_state(ScheduleStates.choosing_forms_education)

        service = UserService(session=session)

        keyboard: InlineKeyboardMarkup = await create_forms_education_kb(
            session=session
        )

        await service.delete_form_education(user_id=callback.from_user.id)

        message = LEXICON["choice_forms_education"]

        sent_message = await callback.message.edit_text(
            text=message, reply_markup=keyboard
        )


@schedule_router.message()
async def process_unknown_message(message: Message):
    """Хендлер для сообщений пользователя, которые не являются командами"""

    logger.info(
        f"Неизвестное сообщение от пользователя {message.from_user.id}: {message.text}"
    )
    await message.delete()
