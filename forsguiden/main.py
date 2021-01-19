import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import List, Optional, Any
from pydantic import BaseModel
import psycopg2.pool

from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import PostgresDb, DbInfo
from forsguiden.db.inmemory import InMemoryDb

from forsguiden.routers.lan import router as lan_router
from forsguiden.routers.vattendrag import router as vattendrag_router
from forsguiden.routers.forsstracka import router as forsstracka_router
from forsguiden.routers.ovrigt import router as ovrigt_router
from forsguiden.auth import AuthError
from forsguiden.security import inloggad, roll

import dotenv

dotenv.load_dotenv()

app: FastAPI = FastAPI(
    title="Forsguiden API",
    description="Målet med Forsguiden API är att samla all information om sveriges forspaddlingsvatten och göra det tillgängligt i ett strukturerat, öppet och väldokumenterat format så att vem som helst ska kunna använda informationen för att bygga egna smarta webapplikationer och mobilappar.",
    version="0.1-ULTRABETA",
)

app.include_router(lan_router)
app.include_router(vattendrag_router)
app.include_router(forsstracka_router)
app.include_router(ovrigt_router)


@app.exception_handler(AuthError)
def handle_auth_error(request: Request, ex: AuthError):
    return JSONResponse(status_code=ex.status_code, content=ex.error)


@app.on_event("startup")
async def startup():
    app.state.pool = psycopg2.pool.ThreadedConnectionPool(
        1, 20, os.environ["DATABASE_URL"]
    )


@app.on_event("shutdown")
async def shutdown():
    app.state.pool.closeall()
