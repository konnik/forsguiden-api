import os
import psycopg2
from sqlalchemy.engine.base import Engine
import sqlalchemy
from sqlalchemy import select

import dotenv
from forsguiden.db.postgres import PostgresDb
from forsguiden.model import *

dotenv.load_dotenv()


psconn = psycopg2.connect(os.environ["DATABASE_URL"])


x = os.environ["DATABASE_URL"].replace("postgres://", "postgresql+psycopg2://")
engine: Engine = sqlalchemy.create_engine(
    os.environ["DATABASE_URL"].replace("postgres://", "postgresql+psycopg2://")
)

f = Forsstracka(
    id=-1,
    namn="Brännsågen-Åbyggeby",
    langd=6000,
    fallhojd=28,
    gradering=Gradering(klass=Grad.tva, lyft=[Grad.tre_plus, Grad.fyra_minus]),
    koordinater=Position(lat=60.75627, long=17.03825),
    flode=Flode(smhipunkt=12020, minimum=20, maximum=100, optimal=30),
    vattendrag=[ForsstrackaVattendrag(id=1, namn="Testeboån")],
    lan=[ForsstrackaLan(id=21, namn="Gävleborg")],
)

db = PostgresDb(psconn, engine)

v = db.hamta_vattendrag(1)
if v is not None:
    print(v.id, v.namn)
    v.namn = v.namn + "!"
    v = db.spara_vattendrag(v)
    print(v.id, v.namn, v.beskrivning[:30], v.lan)
else:
    print("finns ej")

exit(1)

with engine.begin() as c:
    # c.execute("delete from lan where id=99")
    # raise Exception("korv")
    # c.execute("insert into lan (id, lankod, namn) values (99, '99', 'Dummy')")

    r = c.execute("select count(*) from lan").fetchone()
    print(r[0])
