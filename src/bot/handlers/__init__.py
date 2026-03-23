__all__ = (
    "schedule_router",
    "commands_router",
    "admin_panel_router",
)

from .schedule import schedule_router
from .commands import commands_router
from .admin_panel import admin_panel_router
