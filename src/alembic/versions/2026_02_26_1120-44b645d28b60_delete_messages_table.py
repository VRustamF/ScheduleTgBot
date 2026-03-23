"""delete_messages_table

Revision ID: 44b645d28b60
Revises: bd8b5e2c9224
Create Date: 2026-02-26 11:20:54.290395

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "44b645d28b60"
down_revision: Union[str, Sequence[str], None] = "bd8b5e2c9224"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f("ix_bot_messages_message_id"), table_name="bot_messages")
    op.drop_table("bot_messages")
    op.add_column(
        "users",
        sa.Column(
            "is_baned", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_baned")
    op.create_table(
        "bot_messages",
        sa.Column("message_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("chat_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("bot_messages_pkey")),
    )
    op.create_index(
        op.f("ix_bot_messages_message_id"),
        "bot_messages",
        ["message_id"],
        unique=True,
    )
