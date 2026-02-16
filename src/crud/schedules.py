import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db import Subject, DailySchedule, Schedule

logger = logging.getLogger(__file__)


class ScheduleService:
    """Сервис для crud операций над расписанием"""

    def __init__(self, session: AsyncSession):
        """Получаем сессию"""
        self.session = session

    async def get_schedule(
        self,
        form_education: str,
        faculty: str,
        group: str,
        with_details: bool = False,
    ) -> Schedule | None:
        """Функция для получения расписания"""
        stmt = select(Schedule).where(
            Schedule.form_education == form_education,
            Schedule.faculty == faculty,
            Schedule.group == group,
        )

        if with_details:
            stmt = stmt.options(
                selectinload(Schedule.daily_schedules).selectinload(
                    DailySchedule.subjects
                )
            )

        result = await self.session.execute(stmt)
        schedule = result.scalar_one_or_none()

        if not schedule:
            logger.debug(
                f"Расписание для {form_education} {faculty} {group} не найдено"
            )

        return schedule

    def add_schedule(self, form_education: str, faculty: str, group: str) -> Schedule:
        """Добавляет расписание в сессию БЕЗ коммита"""
        schedule = Schedule(
            form_education=form_education,
            faculty=faculty,
            group=group,
        )
        self.session.add(schedule)
        return schedule

    async def create_schedule(
        self, form_education: str, faculty: str, group: str
    ) -> Schedule:
        """Функция для создания расписания"""
        schedule = Schedule(
            form_education=form_education,
            faculty=faculty,
            group=group,
        )
        self.session.add(schedule)

        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при сохранении расписания: {e}")
        await self.session.refresh(schedule)
        return schedule

    async def update_schedule(self):
        """Функция для обновления расписания"""
        pass

    async def delete_schedule(self):
        """Функция для удаления расписания"""
        pass

    async def get_daily_schedule(self):
        """Функция для получения расписания на день"""
        pass

    def add_daily_schedule(self, name: str, schedule_id: int) -> DailySchedule:
        """Функция для создания расписания на день БЕЗ коммита"""
        daily_schedule = DailySchedule(name=name, schedule_id=schedule_id)
        self.session.add(daily_schedule)
        return daily_schedule

    async def update_daily_schedule(self):
        """Функция для обновления расписания на день"""
        pass

    async def delete_daily_schedule(self):
        """Функция для удаления расписания на день"""
        pass

    async def get_subject(self):
        """Функция для получения предмета"""
        pass

    def add_subject(
        self,
        name: str,
        queue_number: int,
        parity: str | None,
        time: str,
        audience: str | None,
        teacher: str | None,
        daily_schedule_id: int,
    ) -> Subject:
        """Функция для создания предмета БЕЗ коммита"""
        subject = Subject(
            name=name,
            queue_number=queue_number,
            parity=parity,
            time=time,
            audience=audience,
            teacher=teacher,
            daily_schedule_id=daily_schedule_id,
        )
        self.session.add(subject)
        return subject

    async def update_subject(self):
        """Функция для обновления предмета"""
        pass

    async def delete_subject(self):
        """Функция для удаления предмета"""
        pass

    async def commit(self):
        """Явный коммит всех накопленных изменений"""
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при сохранении: {e}")
            raise
