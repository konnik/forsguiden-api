import psycopg2
import urllib.parse as urlparse
from db import Db
from typing import List, Optional

class PostgresDb(Db):
    dbname: str
    user: str
    password: str
    host: str
    port: int

    def __init__(self, connection_url: str):
        url = urlparse.urlparse(connection_url)
    
        self.dbname = url.path[1:]
        self.user = url.username or ""
        self.password = url.password or ""
        self.host = url.hostname or ""
        self.port = url.port or 2345

        print(self.dbname, self.user, self.password, self.host, self.port)

    def check(self) -> bool:
        return False