import os
from fastapi import FastAPI, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel
import psycopg2.pool

from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import PostgresDb, DbInfo
from forsguiden.db.inmemory import InMemoryDb

from forsguiden.dependencies import on_database
from forsguiden.routers.lan import router as lan_router
from forsguiden.routers.vattendrag import router as vattendrag_router
from forsguiden.routers.forsstracka import router as forsstracka_router

import dotenv

dotenv.load_dotenv()

app: FastAPI = FastAPI(
    title="Forsguiden API",
    description="Målet med Forsguiden API är att samla all information om sveriges forspaddlingsvatten och göra det tillgängligt i ett strukturerat, öppet och väldokumenterat format så att vem som helst ska kunna använda informationen för att bygga egna smarta webapplikationer och mobilappar.",
    version="0.1-UTRABETA",
)

app.include_router(lan_router)
app.include_router(vattendrag_router)
app.include_router(forsstracka_router)


@app.on_event("startup")
async def startup():
    app.state.pool = psycopg2.pool.ThreadedConnectionPool(
        1, 20, os.environ["DATABASE_URL"]
    )


@app.on_event("shutdown")
async def shutdown():
    app.state.pool.closeall()


# Övrigt


@app.get("/", tags=["Övrigt"])
async def root():
    return {
        "meddelande": "Välkommen till Forsguiden API",
        "swagger": "/docs",
        "resurser": ["/lan", "/vattendrag", "/forsstracka", "/datadump"],
    }


@app.get("/db", tags=["Övrigt"])
async def db_status(db: PostgresDb = Depends(on_database)) -> DbInfo:
    return db.info()


@app.get("/datadump", tags=["Övrigt"])
async def dumpa_allt_data() -> DataDump:
    return DataDump(
        lan=db.lista_lan(),
        vattendrag=db.lista_vattendrag(),
        forsstracka=db.lista_forsstracka(),
    )
