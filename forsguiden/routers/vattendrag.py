from typing import Optional, List

import fastapi
from fastapi import Depends

from forsguiden.dependencies import on_database, on_inMemDb
from forsguiden.model import *
from forsguiden.db import Db

router = fastapi.APIRouter()


# Vattendrag


@router.get("/vattendrag", tags=["Vattendrag"])
async def lista_vattendrag(db: Db = Depends(on_inMemDb)) -> VattendragCollection:
    return VattendragCollection(vattendrag=db.lista_vattendrag())


@router.get("/vattendrag/{id}", tags=["Vattendrag"])
async def hamta_vattendrag_med_id(id: int, db: Db = Depends(on_inMemDb)) -> Vattendrag:
    vattendrag = db.hamta_vattendrag(id)
    if vattendrag is None:
        raise fastapi.HTTPException(status_code=404)
    return vattendrag


@router.post("/vattendrag", tags=["Vattendrag"])
async def skapa_nytt_vattendrag(
    vattendrag: Vattendrag, db: Db = Depends(on_inMemDb)
) -> Vattendrag:
    # ignorera eventuellt id i requestet
    vattendrag.id = -1
    return db.spara_vattendrag(vattendrag)


@router.put("/vattendrag/{id}", tags=["Vattendrag"])
async def uppdatera_vattendrag(
    id: int, vattendrag: Vattendrag, db: Db = Depends(on_inMemDb)
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
