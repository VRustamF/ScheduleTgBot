import logging

from sqlalchemy import select, delete
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

        return schedule

    async def get_forms_education(self) -> list[str | None]:
        """Возвращает список форм обучения"""

        stmt = select(Schedule.form_education).distinct()
        forms_education = await self.session.scalars(stmt)

        return list(forms_education.all())

    async def get_faculties(self, form_education: str) -> list[str | None]:
        """Возвращает список факультетов определенной формы обучения"""

        stmt = (
            select(Schedule.faculty)
            .where(Schedule.form_education == form_education)
            .distinct()
        )
        faculties = await self.session.scalars(stmt)

        return list(faculties.all())

    async def get_groups(
        self,
        form_education: str,
        faculty: str,
    ) -> list[str | None]:
        """Возвращает список групп определенного факультета определенной формы обучения"""

        stmt = (
            select(Schedule.group)
            .where(
                Schedule.form_education == form_education, Schedule.faculty == faculty
            )
            .distinct()
        )
        groups = await self.session.scalars(stmt)

        return list(groups.all())

    async def add_schedule(
        self, form_education: str, faculty: str, group: str
    ) -> Schedule:
        """Добавляет расписание в сессию БЕЗ коммита"""
        schedule = Schedule(
            form_education=form_education,
            faculty=faculty,
            group=group,
        )
        self.session.add(schedule)
        await self.session.flush()
        return schedule

    async def add_daily_schedule(self, name: str, schedule_id: int) -> DailySchedule:
        """Функция для создания расписания на день БЕЗ коммита"""

        daily_schedule = DailySchedule(name=name, schedule_id=schedule_id)
        self.session.add(daily_schedule)
        await self.session.flush()
        return daily_schedule

    async def add_subject(
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
        await self.session.flush()
        return subject

    async def commit(self) -> None:
        """Явный коммит всех накопленных изменений"""

        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при сохранении: {e}")
            raise

    async def clear_schedule_content(self, schedule_id: int) -> None:
        """Удаляет все daily_schedules и subjects для обновления расписания"""

        stmt = delete(DailySchedule).where(DailySchedule.schedule_id == schedule_id)
        await self.session.execute(stmt)
        await self.session.flush()
