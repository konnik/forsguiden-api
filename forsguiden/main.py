import os
from fastapi import FastAPI, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel
import psycopg2.pool

from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import PostgresDb, DbInfo
from forsguiden.db.inmemory import InMemoryDb
import dotenv
dotenv.load_dotenv()

app : FastAPI = FastAPI()

db : InMemoryDb = InMemoryDb(generera_testdata=True)


async def database(request: Request):
    conn = request.app.state.pool.getconn()
    try:
        yield PostgresDb(conn)
    finally:
        request.app.state.pool.putconn(conn)

@app.on_event("startup")
async def startup():
    app.state.pool = psycopg2.pool.ThreadedConnectionPool(1,20,os.environ["DATABASE_URL"]);


@app.on_event("shutdown")
async def shutdown():
    app.state.pool.closeall()


# Län

@app.get("/lan", tags=["Län"])
async def lista_alla_lan(db: Db = Depends(database)) -> LanCollection:
    return LanCollection(lan=db.lista_lan())

@app.get("/lan/{id}", tags=["Län"])
async def hamta_lan_med_id(id: int, db: Db = Depends(database)) -> Lan:
    lan = db.hamta_lan(id)
    if lan is None:
        raise HTTPException(status_code=404)
    return lan

@app.post("/lan", tags=["Län"])
async def skapa_nytt_lan(lan: Lan, db: Db = Depends(database)) -> Lan:
    x : Optional[Lan] = db.hamta_lan(lan.id)
    if x is not None:
        raise HTTPException(status_code = 409, detail= f"Det finns redan ett län med id {x.id}: {x.namn}")
    return db.spara_lan(lan)

@app.put("/lan/{id}", tags=["Län"])
async def uppdatera_lan(id: int, lan: Lan, db: Db = Depends(database)) -> Lan:
    x : Optional[Lan] = db.hamta_lan(id)
    if x is None:
        raise HTTPException(status_code = 404, detail= f"Det finns inget län med id {id}.")

    if lan.id != id:
        raise HTTPException(status_code = 409, detail= f"Länets id kan inte ändras.")

    return db.spara_lan(lan)

@app.delete("/lan/{id}",status_code=204, tags=["Län"])
async def radera_lan(id: int, db: Db = Depends(database)):
    x : Optional[Lan] = db.hamta_lan(id)
    if x is None:
        raise HTTPException(status_code = 404, detail= f"Det finns inget län med id {id}.")

    db.radera_lan(id)

# Vattendrag

@app.get("/vattendrag", tags=["Vattendrag"])
async def lista_vattendrag() -> VattendragCollection:
    return VattendragCollection(vattendrag=db.lista_vattendrag())

@app.get("/vattendrag/{id}", tags=["Vattendrag"])
async def hamta_vattendrag_med_id(id: int) -> Vattendrag:
    vattendrag = db.hamta_vattendrag(id)
    if vattendrag is None:
        raise HTTPException(status_code=404)
    return vattendrag

@app.post("/vattendrag", tags=["Vattendrag"])
async def skapa_nytt_vattendrag(vattendrag: Vattendrag) -> Vattendrag:
    # ignorera eventuellt id i requestet
    vattendrag.id = -1
    return db.spara_vattendrag(vattendrag)

@app.put("/vattendrag/{id}", tags=["Vattendrag"])
async def uppdatera_vattendrag(id: int, vattendrag: Vattendrag) -> Vattendrag:
    x : Optional[Vattendrag] = db.hamta_vattendrag(id)
    if x is None:
        raise HTTPException(status_code = 404, detail= f"Det finns inget vattendrag med id {id}.")

    if vattendrag.id != id:
        raise HTTPException(status_code = 409, detail= f"Vattendragets id kan inte ändras.")

    return db.spara_vattendrag(vattendrag)


# Forssträcka

@app.get("/forsstracka", tags=["Forssträcka"])
async def lista_forsstrackor() -> ForsstrackaCollection:
    return ForsstrackaCollection(forsstracka=db.lista_forsstracka())

@app.get("/forsstracka/{id}", tags=["Forssträcka"])
async def hamta_forsstracka_med_id(id: int) -> Forsstracka:
    forsstracka = db.hamta_forsstracka(id)
    if forsstracka is None:
        raise HTTPException(status_code=404)
    return forsstracka

@app.post("/forsstracka", tags=["Forssträcka"])
async def skapa_ny_forsstracka(forsstracka: Forsstracka) -> Forsstracka:
    # ignorera eventuellt id i requestet
    forsstracka.id = -1
    return db.spara_forsstracka(forsstracka)

@app.put("/forsstracka/{id}", tags=["Forssträcka"])
async def uppdatera_forsstracka(id: int, forsstracka: Forsstracka) -> Forsstracka:
    x : Optional[Forsstracka] = db.hamta_forsstracka(id)
    if x is None:
        raise HTTPException(status_code = 404, detail= f"Det finns inget forsstracka med id {id}.")

    if forsstracka.id != id:
        raise HTTPException(status_code = 409, detail= f"Forssträckans id kan inte ändras.")

    return db.spara_forsstracka(forsstracka)


# Övrigt

@app.get("/", tags=["Övrigt"])
async def root():
    return {
        "meddelande": "Välkommen till Forsguiden API",
        "swagger": "/docs",
        "resurser":["/lan", "/vattendrag", "/forsstracka", "/datadump"]
        }

@app.get("/db", tags=["Övrigt"])
async def db_status( db2: PostgresDb = Depends(database)) -> DbInfo:
    return db2.info()

@app.get("/datadump", tags=["Övrigt"])
async def dumpa_allt_data() -> DataDump:
    return DataDump(lan=db.lista_lan(),
                    vattendrag=db.lista_vattendrag(),
                    forsstracka=db.lista_forsstracka())

