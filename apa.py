import os
import psycopg2
from sqlalchemy.engine.base import Engine
import sqlalchemy
import dotenv
from forsguiden.db.postgres import PostgresDb
from forsguiden.model import *

dotenv.load_dotenv()


psconn = psycopg2.connect(os.environ["DATABASE_URL"])


x = os.environ["DATABASE_URL"].replace("postgres://", "postgresql+psycopg2://")
engine: Engine = sqlalchemy.create_engine(x)

db = PostgresDb(psconn, engine)

print(db.info())