import psycopg2
import urllib.parse as urlparse

from pydantic.main import BaseModel
from forsguiden.db import Db
from typing import List, Optional, Any, Tuple

from forsguiden.model import *


class DbStats(BaseModel):
    lan: int = None


class DbInfo(BaseModel):
    up: bool
    info: str
    stats: Optional[DbStats] = None


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
                    return DbInfo(up=True, info=version, stats=DbStats(lan=antal_lan))

        except psycopg2.Error as e:
            return DbInfo(up=False, info=str(e))

    def lista_lan(self) -> List[Lan]:
        with self.conn.cursor() as cursor:
            cursor.execute("select id, namn from lan;")
            return [_mappa_lan(x) for x in cursor]

    def hamta_lan(self, id: int) -> Optional[Lan]:
        with self.conn.cursor() as cursor:
            cursor.execute("select id, namn from lan where id=%s;", (id,))
            if cursor.rowcount == 0:
                return None
            else:
                return _mappa_lan(cursor.fetchone())

    def spara_lan(self, nytt_lan: Lan) -> Lan:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("delete from lan where id=%s;", (nytt_lan.id,))
                cur.execute(
                    "insert into lan (id, lankod, namn) values (%s, %s, %s);",
                    (nytt_lan.id, f"{nytt_lan.id:02}", nytt_lan.namn),
                )

        return nytt_lan

    def radera_lan(self, id) -> bool:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("delete from lan where id=%s;", (id,))
                antal_raderade = cur.rowcount

        return antal_raderade > 0

    # vattendrag
    def _lan_for_vattendrag(self, id: int) -> List[Lan]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "select id, namn from lan "
                "where id in (select lan_id from vattendrag_lan where vattendrag_id=%s);",
                (id,),
            )
            return [_mappa_lan(x) for x in cursor]

    def lista_vattendrag(self) -> List[Vattendrag]:
        with self.conn.cursor() as cursor:
            cursor.execute("select id, namn, beskrivning from vattendrag;")
            return [
                _mappa_vattendrag((id, namn, beskrivning), self._lan_for_vattendrag(id))
                for (id, namn, beskrivning) in cursor
            ]

    def hamta_vattendrag(self, id: int) -> Optional[Vattendrag]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "select id, namn, beskrivning from vattendrag where id=%s;", (id,)
            )
            if cursor.rowcount == 0:
                return None
            else:
                x = cursor.fetchone()
                (id, _, _) = x
                return _mappa_vattendrag(x, self._lan_for_vattendrag(id))


# mappers


def _mappa_lan(data: Tuple[int, str]) -> Lan:
    (id, namn) = data
    return Lan(id=id, namn=namn)


def _mappa_vattendrag(data: Tuple[int, str, str], lan: List[Lan]) -> Vattendrag:
    (id, namn, beskrivning) = data
    return Vattendrag(
        id=id,
        namn=namn,
        beskrivning=beskrivning,
        lan=lan,
    )