from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor, execute_batch


@contextmanager
def connect_db(*args: any, func: any = psycopg2.connect, **kwargs: any):
    """Метод подключения к базе данных с использованием декоратора контекстного менеджера"""
    conn = func(*args, **kwargs)
    yield conn
    conn.close()


class PostgresSaver:
    def __init__(self, dsn):
        self.dsn = dsn

    async def save_batch_data(self, batch_list: list[dict], *options):
        """Метод записи некоторого числа строк в таблицу БД"""
        with connect_db(**self.dsn) as pg_conn:
            cursor = pg_conn.cursor(cursor_factory=DictCursor)
            query = (
                "INSERT INTO {0} ({1}) VALUES ({2}) ON CONFLICT (id) DO NOTHING".format(
                    *options
                )
            )
            execute_batch(cursor, query, batch_list)
            pg_conn.commit()
