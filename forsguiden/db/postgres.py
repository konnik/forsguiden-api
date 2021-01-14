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

    def hamta_lan(self, id: int) -> Optional[Lan]:
        with self.conn.cursor() as cursor:
            cursor.execute("select id, namn from lan where id=%s;", (id,))
            if cursor.rowcount == 0:
                return None
            else:
                (id, namn) = cursor.fetchone()
                return Lan(id=id, namn=namn)
    
    def spara_lan(self, nytt_lan: Lan) -> Lan:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("delete from lan where id=%s;", (nytt_lan.id,))
                cur.execute("insert into lan (id, lankod, namn) values (%s, %s, %s);", 
                            (nytt_lan.id, f"{nytt_lan.id:02}", nytt_lan.namn))

        return nytt_lan

    def radera_lan(self, id) -> bool:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("delete from lan where id=%s;", (id,))
                antal_raderade = cur.rowcount

        return antal_raderade > 0
