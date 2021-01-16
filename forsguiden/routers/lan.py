from typing import Optional, List

import fastapi
from fastapi import Depends

from forsguiden.dependencies import on_database
from forsguiden.model import *
from forsguiden.db import Db

router = fastapi.APIRouter(tags=["Län"])


@router.get("/lan")
async def lista_alla_lan(db: Db = Depends(on_database)) -> LanCollection:
    return LanCollection(lan=db.lista_lan())


@router.get("/lan/{id}")
async def hamta_lan_med_id(id: int, db: Db = Depends(on_database)) -> Lan:
    lan = db.hamta_lan(id)
    if lan is None:
        raise fastapi.HTTPException(status_code=404)
    return lan


@router.post("/lan")
async def skapa_nytt_lan(lan: Lan, db: Db = Depends(on_database)) -> Lan:
    x: Optional[Lan] = db.hamta_lan(lan.id)
    if x is not None:
        raise fastapi.HTTPException(
            status_code=409, detail=f"Det finns redan ett län med id {x.id}: {x.namn}"
        )
    return db.spara_lan(lan)


@router.put("/lan/{id}")
async def uppdatera_lan(id: int, lan: Lan, db: Db = Depends(on_database)) -> Lan:
    x: Optional[Lan] = db.hamta_lan(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns inget län med id {id}."
        )

    if lan.id != id:
        raise fastapi.HTTPException(
            status_code=409, detail=f"Länets id kan inte ändras."
        )

    return db.spara_lan(lan)


@router.delete("/lan/{id}", status_code=204)
async def radera_lan(id: int, db: Db = Depends(on_database)):
    x: Optional[Lan] = db.hamta_lan(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns inget län med id {id}."
        )

    db.radera_lan(id)
