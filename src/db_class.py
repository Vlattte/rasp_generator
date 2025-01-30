""" Подключение к базе данных из конфига config.ini """

from configparser import ConfigParser
from psycopg2 import connect
from psycopg2 import Error as pg_error
from psycopg2.extras import RealDictCursor


class Database:
    """Класс работы с БД"""

    def __init__(self):
        """Инициализация"""
        self.conn = None
        self.cur = None
        self.set_conn()

    def __del__(self):
        """Очистка"""
        self.close_conn()

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
            self.conn.autocommit = True
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except pg_error:
            print("Set connection error occured", pg_error)
            self.conn = None
            self.cur = None

    def close_conn(self):
        """Закрыть соединение с базой"""
        # если соединение открыто, закрываем
        if self.conn:
            self.cur.close()
            self.conn.close()

    def send_request(self, query: str, is_return: bool = False):
        """отправка запроса query и возврат данных, если is_return == True"""
        try:
            return_data = None
            self.cur.execute(query)
            if is_return:
                return_data = self.cur.fetchall()
            return return_data
        except pg_error:
            print(f"PostgreSQL error occured {pg_error} after request:\n{query}")
            return None

    def get_discs_for_group(self, semcode, group_id):
        """Получить расписание на неделю на семестр и у выбранной группы"""
        query = f"""
        SELECT 
            disc.shorttitle,
            disc.department_id,
            r7.pair,
            r7.weekday,
            r7.weeksarray
            FROM sc_rasp7 r7
        INNER JOIN sc_rasp7_groups r7_gr ON r7.id = r7_gr.rasp7_id 
        INNER JOIN sc_disc disc ON disc.id = r7.disc_id
            WHERE r7.semcode = {semcode} and r7_gr.group_id = {group_id};
        """
        return_data = self.send_request(query, is_return=True)
        return return_data

    def get_groups_data(self):
        """Получить id групп"""
        query = "SELECT id, title from sc_group;"
        return_data = self.send_request(query, is_return=True)
        return return_data
