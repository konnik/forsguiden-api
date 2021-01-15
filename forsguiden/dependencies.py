from fastapi import Request

from forsguiden.db.postgres import PostgresDb
from forsguiden.db.inmemory import InMemoryDb


async def on_inMemDb(request: Request):
    return InMemoryDb(generera_testdata=True)


async def on_database(request: Request):
    conn = request.app.state.pool.getconn()
    try:
        yield PostgresDb(conn)
    finally:
        request.app.state.pool.putconn(conn)
