"""Вспомогательные методы"""

from re import search
from re import fullmatch
from copy import deepcopy
from datetime import datetime, time


def get_lesson_type(lesson: str) -> str:
    """Вытащить тип пары (лк, пр, лб)"""
    lesson_type = "пр"
    lesson_copy = deepcopy(lesson)

    # чтобы избежать опечаток с пробелами, добавляем после всех точек пробел
    # Лин. алг.и ан. геом. -> Лин.алг.и ан.геом.
    lesson_copy = lesson_copy.replace(". ", ".")
    # Лин.алг.и ан.геом.   -> Лин. алг. и ан. геом.
    lesson_copy = lesson_copy.replace(".", ". ")

    if search(r"лк", lesson) is not None:
        lesson_type = "лк"
    if search(r"лб", lesson) is not None:
        lesson_type = "лб"
    return lesson_type


def get_stud_years(title: str):
    """Получить год начала и конца учебного года"""
    today = datetime.now()
    start_year = today.year
    end_year = start_year + 1

    year_pattern = r"20\d\d/\d\d"
    stud_years = search(year_pattern, title)

    if stud_years is not None:
        years_str = stud_years.group()
        start_year = years_str[:4]
        end_year = "20" + years_str[5:]
    return start_year, end_year


def get_stud_period(semcode: int):
    """Формируем границы учебного семестра"""
    season = str(semcode)[:2]
    start_year = str(semcode)[2:4]
    end_year = str(semcode)[4:]
    start_date = ""
    end_date = ""
    # если осенний семестр
    if season == "00":
        start_date = f"20{start_year}-09-01"
        end_date = f"20{end_year}-02-07"
    else:
        start_date = f"20{start_year}-02-07"
        end_date = f"20{end_year}-07-07"
    return start_date, end_date

def get_order_by_time(time_start):
    """Определение номера пары по ее времени"""
    order = 1
    if time_start < time(10, 30):
        order = 1
    elif time_start < time(12, 10):
        order = 2
    elif time_start < time(14, 10):
        order = 3
    elif time_start < time(15, 50):
        order = 4
    elif time_start < time(17, 50):
        order = 5
    elif time_start < time(19, 30):
        order = 6
    else:
        order = 7
    return order


def get_time_by_order(order):
    """Получить время начала пары"""
    time_start = "null"
    match order:
        case 1:
            time_start = time(9, 00)
        case 2:
            time_start = time(10, 40)
        case 3:
            time_start = time(12, 40)
        case 4:
            time_start = time(14, 20)
        case 5:
            time_start = time(16, 20)
        case 6:
            time_start = time(18, 00)
        case 7:
            time_start = time(19, 40)
    return time_start


def time_in_90_minutes(time_start):
    """Получить время через 1.5 часа"""
    end_minutes = (time_start.minute + 30) % 60
    end_hour = time_start.hour + 1

    # если перешли в следующий час
    if end_minutes < 30:
        end_hour += 1
    time_end = time(end_hour, end_minutes)
    return time_end


def is_hsplitter(ws, row) -> bool:
    """Является ли строка горизонтальным разделителем"""
    min_col = ws.min_column
    max_col = ws.max_column
    for col in range(min_col, max_col):
        if ws.cell(row, col).value is not None:
            return False
    return True


def get_version(rasp_title: str):
    """Получить версию расписания из главного заголовка"""
    version_begin = rasp_title.index("версия")
    version_str = rasp_title[version_begin:]  # версия 13 от 27.10.2024
    VERSION_NUM_POS = 1
    version = version_str.split(" ")[VERSION_NUM_POS]
    return version


def get_worktype(disc_type: str):
    """Получить id типа дисциплины по строковому представлению:
    - 0-пр, 1-лк, 2-лб
    - 10-конс, 11-экз, 12-зaч, 13-зaч-д
    - 14-кр, 15-кп
    """
    # изначально без типа пары
    worktype_id = -1
    match disc_type:
        # просто пары
        case "пр":
            worktype_id = 0
        case "лк":
            worktype_id = 1
        case "лб":
            worktype_id = 2
        # экзамены
        case "конс.":
            worktype_id = 10
        case "экзамен":
            worktype_id = 11
        case "зачет":
            worktype_id = 12
        case "зачет-д":
            worktype_id = 13
        # сдача работ
        case "к/р":
            worktype_id = 14
        case "к/п":
            worktype_id = 15
    return worktype_id


def swap_with_prev_value(prev_val, cur_val):
    """Если текущее значение None, присвоить ему предыдущее, иначе сохранить в предыдущее"""
    prev = prev_val
    cur = cur_val
    if not cur:
        cur = prev
    else:
        prev = cur
    return prev, cur

def get_lesson_count(merged_cells, coord) -> int:
    """Если это пара как НИР или военка(смерджено около 4-5 пар), то вернуть число пар"""
    merged_range = None
    if coord in merged_cells:
        coord_pattern = coord + r':\w+\d+'
        merged_cells_list = merged_cells.sorted()
        merged_range = None
        for cell_range in merged_cells_list:
            if fullmatch(coord_pattern, cell_range.coord):
                merged_range = cell_range
                break
    if merged_range is None:
        return 1

    # смотрим низкую строку, чтобы посчитать сколько нужно пар
    lesson_count = merged_range.max_row - merged_range.min_row
    if  lesson_count > 2:
        lesson_count += 1
        # делим на 2, так как каждая ячейка содержит четную и нечетные недели
        return int(lesson_count/2)
    return 1
