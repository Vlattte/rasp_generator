"""Генерация расписания в xlsx формате"""

from os.path import exists as path_exists

from configparser import ConfigParser
from .db_class import Database

import pandas as pd
from openpyxl import Workbook


class RaspGenerator:
    """Класс генератора расписания, по данным загруженным в БД"""

    def __init__(self):
        """Инициализация генератора"""
        config = ConfigParser()
        config.read("config.ini")
        self.semcode = config["RASP_PARAMS"]["semcode"]
        self.version = config["RASP_PARAMS"]["version"]
        self.version_date = config["RASP_PARAMS"]["version_date"]

        self.db_conn = Database()

    def generate_rasp(self):
        """Сгенерировать расписание"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Занятия"
        

        # TODO Шапка расписания
        self.create_rasp_title(ws)
        wb.save("new_rasp.xlsx")
        return 
        groups_rasp = self.get_week_groups_rasp()
        for g_rasp in groups_rasp:
            self.fill_group_week(g_rasp)


    def create_rasp_title(self, ws):
        """Заполняем шапку"""
        semcode_data = self.get_semcode_data()
        rasp_title = f"""РАСПИСАНИЕ  ЗАНЯТИЙ  НА  {semcode_data["season"]}  СЕМЕСТР
 {semcode_data["years"]}  УЧЕБНОГО  ГОДА\nверсия {self.version} от {self.version_date}"""
        rasp_title.replace("\n ", " ")
        ws.cell(1, 1).value = rasp_title

    def get_semcode_data(self):
        """Сезон года по коду семестра"""
        semcode_data = {"season": "ОСЕННИЙ", "years": "2024/25"}
        season_code = str(self.semcode)[:-2]
        if season_code == "01":
            semcode_data["season"] = "ВЕСЕННИЙ"
        semcode_years = str(self.semcode)[:4]
        semcode_data["years"] = f"20{semcode_years[:2]}/{semcode_years[2:]}"
        return semcode_data

    def get_week_groups_rasp(self):
        """Получить раписание для всех групп обоих подгрупп на неделю"""
        group_data = self.db_conn.get_groups_data()
        print(group_data)
        group_rasp = {}
        for group in group_data:
            g_rasp = self.db_conn.get_discs_for_group(self.semcode, group["id"])
            group_rasp[group["title"]] = g_rasp
        return group_rasp

    def fill_group_week(self, group_rasp):
        """Заполняем расписание для группы на неделю"""
        if group_rasp is None:
            return
