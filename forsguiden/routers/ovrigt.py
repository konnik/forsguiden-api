from typing import Optional, List

import fastapi
from fastapi import Depends

from forsguiden.dependencies import on_database
from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import DbInfo

router = fastapi.APIRouter()

# Övrigt


@router.get("/", tags=["Övrigt"])
async def root():
    return {
        "meddelande": "Välkommen till Forsguiden API",
        "swagger": "/docs",
        "resurser": ["/lan", "/vattendrag", "/forsstracka", "/datadump"],
    }


@router.get("/db", tags=["Övrigt"])
async def db_status(db: Db = Depends(on_database)) -> DbInfo:
    return db.info()


@router.get("/datadump", tags=["Övrigt"])
async def dumpa_allt_data(db: Db = Depends(on_database)) -> DataDump:
    return DataDump(
        lan=db.lista_lan(),
        vattendrag=db.lista_vattendrag(),
        forsstracka=db.lista_forsstracka(),
    )
