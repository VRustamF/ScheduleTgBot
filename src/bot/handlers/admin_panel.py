import logging

from aiogram import Router

admin_panel_router = Router()

logger = logging.getLogger(__name__)

# Фильтр для проверки прав администратора
