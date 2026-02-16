from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(unique=True, index=True)
    first_name: Mapped[str | None]
    username: Mapped[str | None]
    form_education: Mapped[str | None]
    faculty: Mapped[str | None]
    group: Mapped[str | None]

    def __repr__(self):
        return f"User {self.id}: user_id={self.user_id}, username={self.username}"


class BotMessage(Base):
    __tablename__ = "bot_messages"

    message_id: Mapped[int] = mapped_column(unique=True, index=True)
    chat_id: Mapped[int]

    def __repr__(self):
        return f"BotMessage {self.id}: message_id={self.message_id}, chat_id={self.chat_id}"


class Subject(Base):
    __tablename__ = "subjects"

    name: Mapped[str]
    queue_number: Mapped[int]
    parity: Mapped[int | None]
    time: Mapped[str]
    audience: Mapped[str | None]
    teacher: Mapped[str | None]

    daily_schedule_id: Mapped[int] = mapped_column(
        ForeignKey("daily_schedules.id", ondelete="CASCADE")
    )
    daily_schedule: Mapped["DailySchedule"] = relationship(
        back_populates="subjects", lazy="selectin"
    )

    def __repr__(self):
        return f"Subject {self.id}: {self.name} at {self.time}"


class DailySchedule(Base):
    __tablename__ = "daily_schedules"

    name: Mapped[str]
    subjects: Mapped[List["Subject"]] = relationship(
        back_populates="daily_schedule", lazy="selectin"
    )

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE")
    )
    schedule: Mapped["Schedule"] = relationship(
        back_populates="daily_schedules", lazy="selectin"
    )

    def __repr__(self):
        return f"DailySchedule {self.id}: {self.name}"


class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = (
        UniqueConstraint(
            "form_education", "faculty", "group", name="uq_schedule_group"
        ),
    )

    form_education: Mapped[str]
    faculty: Mapped[str]
    group: Mapped[str]
    daily_schedules: Mapped[List["DailySchedule"]] = relationship(
        back_populates="schedule", lazy="selectin"
    )

    def __repr__(self):
        return f"Schedule {self.id}: {self.form_education} {self.faculty} {self.group}"
