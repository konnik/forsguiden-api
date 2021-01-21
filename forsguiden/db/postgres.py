import psycopg2
import urllib.parse as urlparse
import re

from pydantic.main import BaseModel
from forsguiden.db import Db
from typing import List, Optional, Any, Tuple

from forsguiden.model import *


class DbStats(BaseModel):
    lan: int
    vattendrag: int
    forsstrackor: int


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
                    cursor.execute("select count(*) from vattendrag;")
                    (antal_vattendrag,) = cursor.fetchone()
                    cursor.execute("select count(*) from forsstracka;")
                    (antal_forsstrackor,) = cursor.fetchone()
                    return DbInfo(
                        up=True,
                        info=version,
                        stats=DbStats(
                            lan=antal_lan,
                            vattendrag=antal_vattendrag,
                            forsstrackor=antal_forsstrackor,
                        ),
                    )

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
        with self.conn as c:
            with c.cursor() as cur:
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

    def spara_vattendrag(self, nytt_vattendrag: Vattendrag) -> Vattendrag:
        with self.conn as c:  # det här hoppas jag skapar en ny transaktion :)
            with c.cursor() as cursor:
                cursor.execute(
                    "delete from vattendrag_lan where vattendrag_id=%s",
                    (nytt_vattendrag.id,),
                )
                cursor.execute(
                    "delete from vattendrag where id=%s",
                    (nytt_vattendrag.id,),
                )
                if nytt_vattendrag.id == -1:
                    cursor.execute(
                        "insert into vattendrag (namn, beskrivning) values (%s, %s) returning id",
                        (nytt_vattendrag.namn, nytt_vattendrag.beskrivning),
                    )
                    nytt_vattendrag.id = cursor.fetchone()[0]
                else:
                    cursor.execute(
                        "insert into vattendrag (id, namn, beskrivning) values (%s,%s, %s) returning id",
                        (
                            nytt_vattendrag.id,
                            nytt_vattendrag.namn,
                            nytt_vattendrag.beskrivning,
                        ),
                    )

                # spara mappning till län
                for lan in nytt_vattendrag.lan:
                    cursor.execute(
                        "insert into vattendrag_lan (vattendrag_id, lan_id) values (%s, %s)",
                        (nytt_vattendrag.id, lan.id),
                    )

        return self.hamta_vattendrag(nytt_vattendrag.id)

    def radera_vattendrag(self, id: int) -> bool:
        with self.conn as c:
            with c.cursor() as cursor:
                cursor.execute(
                    "delete from vattendrag_lan where vattendrag_id=%s",
                    (id,),
                )
                cursor.execute(
                    "delete from vattendrag where id=%s",
                    (id,),
                )
                antal_raderade = cursor.rowcount

        return antal_raderade > 0

    # forsstracka
    def lista_forsstracka(self) -> List[Forsstracka]:
        with self.conn.cursor() as c:
            c.execute(
                "select id, namn, langd, fallhojd, gradering_klass, gradering_lyft, koord_lat, koord_long, flode_smhipunkt, flode_minimum, flode_optimal, flode_maximum from forsstracka"
            )
            with self.conn.cursor() as c2:
                return [
                    _mappa_forsstracka(
                        x,
                        _fetch_forstracka_lan(x[0], c2),
                        _fetch_forstracka_vattendrag(x[0], c2),
                    )
                    for x in c
                ]

    def hamta_forsstracka(self, id: int) -> Optional[Forsstracka]:
        with self.conn.cursor() as cursor:
            lan = _fetch_forstracka_lan(id, cursor)
            vattendrag = _fetch_forstracka_vattendrag(id, cursor)

            cursor.execute(
                "select id, namn, langd, fallhojd, gradering_klass, gradering_lyft, koord_lat, koord_long, flode_smhipunkt, flode_minimum, flode_optimal, flode_maximum from forsstracka where id=%s",
                (id,),
            )
            if cursor.rowcount == 0:
                return None
            else:
                x = cursor.fetchone()
                return _mappa_forsstracka(x, lan, vattendrag)

    def spara_forsstracka(self, fors: Forsstracka) -> Forsstracka:
        with self.conn as conn:
            with conn.cursor() as c:
                c.execute(
                    "delete from forsstracka_lan where forsstracka_id=%s", (fors.id,)
                )
                c.execute(
                    "delete from forsstracka_vattendrag where forsstracka_id=%s",
                    (fors.id,),
                )
                c.execute("delete from forsstracka where id=%s", (fors.id,))

                values = fors.dict()
                values["gradering_klass"] = fors.gradering.klass
                values["gradering_lyft"] = fors.gradering.lyft
                values["koord_lat"] = fors.koordinater.lat
                values["koord_long"] = fors.koordinater.long
                values["flode_smhipunkt"] = fors.flode.smhipunkt
                values["flode_minimum"] = fors.flode.minimum
                values["flode_maximum"] = fors.flode.maximum
                values["flode_optimal"] = fors.flode.optimal
                if fors.id == -1:
                    c.execute(
                        "insert into forsstracka (namn, langd, fallhojd, gradering_klass, gradering_lyft, koord_lat, koord_long, flode_smhipunkt, flode_minimum, flode_optimal, flode_maximum )"
                        " values (%(namn)s, %(langd)s, %(fallhojd)s, %(gradering_klass)s, %(gradering_lyft)s::klass[], %(koord_lat)s, %(koord_long)s, %(flode_smhipunkt)s, %(flode_minimum)s, %(flode_optimal)s, %(flode_maximum)s)"
                        " returning id",
                        values,
                    )
                    fors.id = c.fetchone()[0]

                else:
                    c.execute(
                        "insert into forsstracka (id, namn, langd, fallhojd, gradering_klass, gradering_lyft, koord_lat, koord_long, flode_smhipunkt, flode_minimum, flode_optimal, flode_maximum )"
                        " values (%(id)s, %(namn)s, %(langd)s, %(fallhojd)s, %(gradering_klass)s, %(gradering_lyft)s::klass[], %(koord_lat)s, %(koord_long)s, %(flode_smhipunkt)s, %(flode_minimum)s, %(flode_optimal)s, %(flode_maximum)s)"
                        "returning id",
                        values,
                    )

                for lan in fors.lan:
                    c.execute(
                        "insert into forsstracka_lan (forsstracka_id, lan_id) values (%s, %s)",
                        (fors.id, lan.id),
                    )

                for vattendrag in fors.vattendrag:
                    c.execute(
                        "insert into forsstracka_vattendrag (forsstracka_id, vattendrag_id) values (%s, %s)",
                        (fors.id, vattendrag.id),
                    )

        return self.hamta_forsstracka(fors.id)

    def radera_forsstracka(self, id: int) -> bool:
        with self.conn as c:
            with c.cursor() as cursor:
                cursor.execute(
                    "delete from forsstracka_lan where forsstracka_id=%s",
                    (id,),
                )
                cursor.execute(
                    "delete from forsstracka_vattendrag where forsstracka_id=%s",
                    (id,),
                )
                cursor.execute(
                    "delete from forsstracka where id=%s",
                    (id,),
                )
                antal_raderade = cursor.rowcount

        return antal_raderade > 0


# fetchers (haha, vafan är det för nåt? :)


def _fetch_forstracka_lan(id, cursor) -> List[ForsstrackaLan]:
    cursor.execute(
        "select id, namn from lan where id in (select lan_id from forsstracka_lan where forsstracka_id=%s)",
        (id,),
    )
    return [ForsstrackaLan(id=lan_id, namn=lan_namn) for (lan_id, lan_namn) in cursor]


def _fetch_forstracka_vattendrag(id, cursor) -> List[ForsstrackaVattendrag]:
    cursor.execute(
        "select id, namn from vattendrag where id in (select vattendrag_id from forsstracka_vattendrag where forsstracka_id=%s)",
        (id,),
    )
    return [ForsstrackaVattendrag(id=id, namn=namn) for (id, namn) in cursor]


# mappers


def _mappa_forsstracka(
    data: Tuple[int, str, int, int, Grad, List[Grad], float, float, int, int, int, int],
    lan: List[ForsstrackaLan],
    vattendrag: List[ForsstrackaVattendrag],
) -> Forsstracka:
    (
        id,
        namn,
        langd,
        fallhojd,
        gradering_klass,
        gradering_lyft,
        koord_lat,
        koord_long,
        flode_smhipunkt,
        flode_minimum,
        flode_optimal,
        flode_maximum,
    ) = data

    def array_of_enum(value):
        inner = re.match(r"^{(.*)}$", value).group(1)
        return inner.split(",") if inner else []

    return Forsstracka(
        id=id,
        namn=namn,
        langd=langd,
        fallhojd=fallhojd,
        gradering=Gradering(
            klass=Grad(gradering_klass), lyft=array_of_enum(gradering_lyft)
        ),
        koordinater=Position(lat=koord_lat, long=koord_long),
        flode=Flode(
            smhipunkt=flode_smhipunkt,
            minimum=flode_minimum,
            maximum=flode_maximum,
            optimal=flode_optimal,
        ),
        vattendrag=vattendrag,
        lan=lan,
    )


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