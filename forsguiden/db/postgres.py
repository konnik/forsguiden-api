import psycopg2
import urllib.parse as urlparse

from pydantic.main import BaseModel
from forsguiden.db import Db
from typing import List, Optional, Any

from forsguiden.model import *

class DbInfo(BaseModel):
    up: bool
    info: str
    lan: int


class PostgresDb(Db):
    conn: Any

    def __init__(self, connection):
        self.conn = connection

    def info(self) -> DbInfo:
        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute("select version();")
                    (version,) = cursor.fetchone()
                    cursor.execute("select count(*) from lan;")
                    (antal_lan,) = cursor.fetchone()
                    return DbInfo(up=True, info = version, lan=antal_lan)

        except psycopg2.Error as e:
            return DbInfo(up=False, info = str(e))


    def lista_lan(self) -> List[Lan]:
        with self.conn.cursor() as cursor:
            cursor.execute("select id, namn from lan;")
            return [ Lan(id=id, namn=namn) for (id, namn) in cursor] 
