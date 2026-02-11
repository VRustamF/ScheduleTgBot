import xlrd
from xlrd import Book

import openpyxl
from openpyxl import Workbook

from data import settings, BASE_DIR


FILES_PATH = f"{BASE_DIR}{settings.schedule.path}"


def copy_merge_cells_to_xlsx(s_name: str, book: Book) -> Workbook:
    """Функция, которая переносит объединенные ячейки из xls в xlsx"""

    sheet = book.sheet_by_name(s_name)

    # создаём xlsx
    wb = openpyxl.Workbook()
    ws = wb.active

    # копируем значения (не обязательно, но обычно нужно)
    for r in range(7, sheet.nrows):
        for c in range(sheet.ncols):
            ws.cell(row=r - 7 + 1, column=c + 1).value = sheet.cell_value(r, c)

    # переносим merged cells
    for r1, r2, c1, c2 in sheet.merged_cells:
        # полностью выше данных -> пропускаем
        if r2 <= 7:
            continue

        # подрезаем merge, если он начинается выше 8 строки
        new_r1 = max(r1, 7)
        new_r2 = r2

        ws.merge_cells(
            start_row=new_r1 - 7 + 1,
            end_row=new_r2 - 7,
            start_column=c1 + 1,
            end_column=c2
        )
    return wb


def formatter() -> None:
    """
    Позволяет конвертировать xls в xlsx без потери объединенных ячеек.
    Создает для каждого листа отдельную таблицу
    """

    # читаем xls
    book = xlrd.open_workbook(
        filename=f"{FILES_PATH}{settings.schedule.file_name}",
        formatting_info=True
    )
    sheet_names = book.sheet_names()

    for s_name in sheet_names:
        workbook: Workbook = copy_merge_cells_to_xlsx(s_name=s_name, book=book)
        workbook.save(f"{FILES_PATH}{s_name}.xlsx")