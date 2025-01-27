""" Подключение к базе данных из конфига config.ini """

from configparser import ConfigParser
from psycopg2 import connect
from psycopg2 import Error as pg_error


class Database:
    """Класс работы с БД"""

    def __init__(self):
        """Инициализация"""
        self.conn = None
        self.cur = None
        self.set_conn()

    def set_conn(self):
        """Установка соединения по данным из конфиг файла"""
        config = ConfigParser()
        config.read("config.ini")

        # параметры подключения к БД
        try:
            self.conn = connect(
                database=config["postgres"]["db_name"],
                user=config["postgres"]["db_user"],
                host=config["postgres"]["db_host"],
                port=config["postgres"]["db_port"],
                password=config["postgres"]["db_password"],
            )
            self.cur = self.conn.cursor()
        except pg_error:
            print("Set connection error occured", pg_error)
            self.conn = None
            self.cur = None
