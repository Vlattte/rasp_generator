"""Генерация расписания в xlsx формате"""

from configparser import ConfigParser


class RaspGenerator:
    """Класс генератора расписания, по данным загруженным в БД"""

    def __init__(self):
        """Инициализация генератора"""
        config = ConfigParser()
        config.read("config.ini")
        self.semcode = config["RASP_PARAMS"]["semcode"]
        
    def get_week_rasp(self):
        """Получить раписание для всех групп обоих подгрупп на неделю"""
                
