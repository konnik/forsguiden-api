from typing import Optional, List

import fastapi
from fastapi import Depends

from forsguiden.dependencies import on_database, on_inMemDb
from forsguiden.model import *
from forsguiden.db import Db

router = fastapi.APIRouter(tags=["Forssträcka"])

# Forssträcka


@router.get("/forsstracka")
async def lista_forsstrackor(db: Db = Depends(on_inMemDb)) -> ForsstrackaCollection:
    return ForsstrackaCollection(forsstracka=db.lista_forsstracka())


@router.get("/forsstracka/{id}")
async def hamta_forsstracka_med_id(
    id: int, db: Db = Depends(on_inMemDb)
) -> Forsstracka:
    forsstracka = db.hamta_forsstracka(id)
    if forsstracka is None:
        raise fastapi.HTTPException(status_code=404)
    return forsstracka


@router.post("/forsstracka")
async def skapa_ny_forsstracka(
    forsstracka: Forsstracka, db: Db = Depends(on_inMemDb)
) -> Forsstracka:
    # ignorera eventuellt id i requestet
    forsstracka.id = -1
    return db.spara_forsstracka(forsstracka)


@router.put("/forsstracka/{id}")
async def uppdatera_forsstracka(
    id: int, forsstracka: Forsstracka, db: Db = Depends(on_inMemDb)
) -> Forsstracka:
    x: Optional[Forsstracka] = db.hamta_forsstracka(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns inget forsstracka med id {id}."
        )

    if forsstracka.id != id:
        raise fastapi.HTTPException(
            status_code=409, detail=f"Forssträckans id kan inte ändras."
        )

    return db.spara_forsstracka(forsstracka)
