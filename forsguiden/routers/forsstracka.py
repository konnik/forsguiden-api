from typing import Optional, List

import fastapi
from fastapi import Depends, Security

from forsguiden.dependencies import on_database
from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.security import behorighet

router = fastapi.APIRouter(tags=["Forssträcka"])

# Forssträcka

_redigera = dependencies = [Security(behorighet("redigera:forsstracka"))]


@router.get("/forsstracka")
async def lista_forsstrackor(db: Db = Depends(on_database)) -> ForsstrackaCollection:
    return ForsstrackaCollection(forsstracka=db.lista_forsstracka())


@router.get("/forsstracka/{id}")
async def hamta_forsstracka_med_id(
    id: int, db: Db = Depends(on_database)
) -> Forsstracka:
    forsstracka = db.hamta_forsstracka(id)
    if forsstracka is None:
        raise fastapi.HTTPException(status_code=404)
    return forsstracka


@router.post("/forsstracka", dependencies=_redigera)
async def skapa_ny_forsstracka(
    forsstracka: Forsstracka, db: Db = Depends(on_database)
) -> Forsstracka:
    if forsstracka.id is None:
        return db.spara_forsstracka(forsstracka)
    else:
        x: Optional[Forsstracka] = db.hamta_forsstracka(forsstracka.id)
        if x is not None:
            raise fastapi.HTTPException(
                status_code=409,
                detail=f"Det finns redan en forsstracka med id {forsstracka.id}.",
            )
        return db.spara_forsstracka(forsstracka)


@router.put(
    "/forsstracka/{id}",
    dependencies=_redigera,
)
async def uppdatera_forsstracka(
    id: int, forsstracka: Forsstracka, db: Db = Depends(on_database)
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


@router.delete(
    "/forsstracka/{id}",
    status_code=204,
    dependencies=_redigera,
)
async def radera_forsstracka(id: int, db: Db = Depends(on_database)):
    x: Optional[Forsstracka] = db.hamta_forsstracka(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns ingen forssträcka med id {id}."
        )

    db.radera_forsstracka(id)


# forssträcka beskrivning


@router.get("/forsstracka/{id}/beskrivning")
async def hamta_forsstracka_beskrivning(
    id: int, db: Db = Depends(on_database)
) -> Optional[ForsstrackaBeskrivning]:
    forsstracka_beskr = db.hamta_forsstracka_beskrivning(id)
    if forsstracka_beskr is None:
        raise fastapi.HTTPException(status_code=404)
    return forsstracka_beskr


@router.put(
    "/forsstracka/{id}/beskrivning",
    dependencies=_redigera,
)
async def uppdatera_forsstracka_beskrivnin(
    id: int, beskrivning: NyForsstrackaBeskrivning, db: Db = Depends(on_database)
) -> ForsstrackaBeskrivning:
    x: Optional[Forsstracka] = db.hamta_forsstracka(id)
    if x is None:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Det finns inget forsstracka med id {id}."
        )

    beskr: ForsstrackaBeskrivning = ForsstrackaBeskrivning(
        beskrivning=beskrivning.beskrivning,
        uppdaterad=datetime.datetime.now(tz=datetime.timezone.utc),
        uppdaterad_av="???",
    )
    return db.spara_forsstracka_beskrivning(id, beskr)
