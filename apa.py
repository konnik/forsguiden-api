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

db = PostgresDb(psconn, engine)

with engine.begin() as c:
    # c.execute("delete from lan where id=99")
    # raise Exception("korv")
    # c.execute("insert into lan (id, lankod, namn) values (99, '99', 'Dummy')")

    r = c.execute("select count(*) from lan").fetchone()
    print(r[0])
