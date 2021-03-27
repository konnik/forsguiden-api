from typing import Optional, List
from urllib.request import urlopen
import fastapi
from fastapi import Depends
from six.moves import urllib

from forsguiden.dependencies import on_database
from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import DbInfo, PostgresDb
from forsguiden.security import behorighet, inloggad

from forsguiden.smhi import sok_smhipunkt

router = fastapi.APIRouter(tags=["Övrigt"])

# Övrigt


@router.get("/")
async def root():
    return {
        "meddelande": "Välkommen till Forsguiden API",
        "swagger": "/docs",
        "resurser": ["/lan", "/vattendrag", "/forsstracka", "/datadump"],
    }


@router.get("/smhipunkt/")
async def smhipunkt(x: float, y: float) -> str:
    p = sok_smhipunkt(x, y)
    if p is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Hittade ingen smhipunkt för koordinat x={x}, y={y}.",
        )
    else:
        return p


@router.get("/hemlig", dependencies=[Depends(behorighet("lasa:hemlighet"))])
async def hemlig():
    return {"meddelande": "Superhemligt..."}


@router.get(
    "/hemlig2",
    dependencies=[Depends(behorighet("lasa:hemlighet"))],
)
async def hemlig2(token=Depends(inloggad())):
    return {"meddelande": "Superhemligt meddelande till: {}".format(str(token))}


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
