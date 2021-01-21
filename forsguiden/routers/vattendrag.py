from typing import Optional, List

import fastapi
from fastapi import Depends, Security

from forsguiden.dependencies import on_database
from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.security import behorighet

router = fastapi.APIRouter(tags=["Vattendrag"])


# Vattendrag
_redigera = dependencies = [Security(behorighet("redigera:vattendrag"))]


@router.get("/vattendrag")
async def lista_vattendrag(db: Db = Depends(on_database)) -> VattendragCollection:
    return VattendragCollection(vattendrag=db.lista_vattendrag())


@router.get("/vattendrag/{id}")
async def hamta_vattendrag_med_id(id: int, db: Db = Depends(on_database)) -> Vattendrag:
    vattendrag = db.hamta_vattendrag(id)
    if vattendrag is None:
        raise fastapi.HTTPException(status_code=404)
    return vattendrag


@router.post("/vattendrag", dependencies=_redigera)
async def skapa_nytt_vattendrag(
    vattendrag: Vattendrag, db: Db = Depends(on_database)
) -> Vattendrag:
    # ignorera eventuellt id i requestet
    vattendrag.id = -1
    return db.spara_vattendrag(vattendrag)


@router.put("/vattendrag/{id}", dependencies=_redigera)
async def uppdatera_vattendrag(
    id: int, vattendrag: Vattendrag, db: Db = Depends(on_database)
) -> Vattendrag:
    x: Optional[Vattendrag] = db.hamta_vattendrag(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns inget vattendrag med id {id}."
        )

    if vattendrag.id != id:
        raise fastapi.HTTPException(
            status_code=409, detail=f"Vattendragets id kan inte ändras."
        )

    return db.spara_vattendrag(vattendrag)


@router.delete(
    "/vattendrag/{id}",
    status_code=204,
    dependencies=_redigera,
)
async def radera_vattendrag(id: int, db: Db = Depends(on_database)):
    x: Optional[Vattendrag] = db.hamta_vattendrag(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns inget vattendrag med id {id}."
        )

    db.radera_vattendrag(id)
