"""init db

Revision ID: 6f8801395d90
Revises:
Create Date: 2026-02-16 14:36:03.812043

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6f8801395d90"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "bot_messages",
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bot_messages_message_id"),
        "bot_messages",
        ["message_id"],
        unique=True,
    )
    op.create_table(
        "schedules",
        sa.Column("form_education", sa.String(), nullable=False),
        sa.Column("faculty", sa.String(), nullable=False),
        sa.Column("group", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "form_education", "faculty", "group", name="uq_schedule_group"
        ),
    )
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("form_education", sa.String(), nullable=True),
        sa.Column("faculty", sa.String(), nullable=True),
        sa.Column("group", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_user_id"), "users", ["user_id"], unique=True)
    op.create_table(
        "daily_schedules",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("schedule_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subjects",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("queue_number", sa.Integer(), nullable=False),
        sa.Column("parity", sa.Integer(), nullable=True),
        sa.Column("time", sa.String(), nullable=False),
        sa.Column("audience", sa.String(), nullable=True),
        sa.Column("teacher", sa.String(), nullable=True),
        sa.Column("daily_schedule_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["daily_schedule_id"], ["daily_schedules.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("subjects")
    op.drop_table("daily_schedules")
    op.drop_index(op.f("ix_users_user_id"), table_name="users")
    op.drop_table("users")
    op.drop_table("schedules")
    op.drop_index(op.f("ix_bot_messages_message_id"), table_name="bot_messages")
    op.drop_table("bot_messages")
