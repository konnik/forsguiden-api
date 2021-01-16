from typing import Optional, List

import fastapi
from fastapi import Depends

from forsguiden.dependencies import on_database
from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import DbInfo, PostgresDb
from forsguiden.security import roll, inloggad

router = fastapi.APIRouter(tags=["Övrigt"])

# Övrigt


@router.get("/")
async def root():
    return {
        "meddelande": "Välkommen till Forsguiden API",
        "swagger": "/docs",
        "resurser": ["/lan", "/vattendrag", "/forsstracka", "/datadump"],
    }


@router.get("/hemlig", dependencies=[Depends(inloggad()), Depends(roll("korv"))])
async def hemlig():
    return {"meddelande": "Superhemligt..."}


@router.get("/db")
async def db_status(db: PostgresDb = Depends(on_database)) -> DbInfo:
    return db.info()


@router.get("/datadump")
async def dumpa_allt_data(db: Db = Depends(on_database)) -> DataDump:
    return DataDump(
        lan=db.lista_lan(),
        vattendrag=db.lista_vattendrag(),
        forsstracka=db.lista_forsstracka(),
    )
