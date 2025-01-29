"""Цвета расписания"""

from enum import Enum
from openpyxl.styles.colors import Color


class CellColors:
    """Цвета ячеек"""
    # общее оформление
    BORDER = Color(rgb="FF595959")
    TITLE = Color(rgb="FF000000")
    ORDER = Color(rgb="FFD9D9D9")
    # кафедры
    OTHERS_DEP = Color(rgb="FFD1F3FF")   # едут другие кафедры
    VM_DEP = Color(rgb="FFFFF56D")       # ведет ВМ
    VEGA_DEP = Color(rgb="FFEAFF9F")     # ведет ВЕГА
    ONLY_VM_DEP = Color(rgb="FFFFCCFF")  # только для подгруппы ВМ
