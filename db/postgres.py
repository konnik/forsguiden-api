from re import VERBOSE
import psycopg2
import urllib.parse as urlparse

from pydantic.main import BaseModel
from db import Db
from typing import List, Optional, Any

class DbInfo(BaseModel):
    up: bool
    info: str


class PostgresDb(Db):
    database: Optional[str]
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]

    def __init__(self, connection_url: str):
        url = urlparse.urlparse(connection_url)
    
        self.database = url.path[1:]
        self.username = url.username
        self.password = url.password
        self.host = url.hostname
        self.port = url.port

    def info(self) -> DbInfo:
        connection = None
        cursor : Any = None
        try:
            connection = psycopg2.connect(user=self.username,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)

            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            (version,) = cursor.fetchone()
            return DbInfo(up=True, info = version)

        except psycopg2.Error as e:
            return DbInfo(up=False, info = str(e))
        finally:
            if (connection):
                cursor.close()
                connection.close()