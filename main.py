import os
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from model import *
from db.postgres import PostgresDb
from db.inmemory import InMemoryDb


db : InMemoryDb = InMemoryDb()
db2 : PostgresDb = PostgresDb(os.getenv("DATABASE_URL", ""))

app : FastAPI = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/db")
async def db_status():
    return {"up": db2.check()}

# län

@app.get("/lan")
async def lista_alla_lan() -> LanCollection:
    return LanCollection(lan=db.lista_lan())

@app.get("/lan/{id}")
async def hamta_lan_med_id(id: int) -> Lan:
    lan = db.hamta_lan(id)
    if lan is None:
        raise HTTPException(status_code=404)
    return lan

@app.post("/lan")
async def skapa_nytt_lan(lan: Lan) -> Lan:
    x : Optional[Lan] = db.hamta_lan(lan.id)
    if x is not None:
        raise HTTPException(status_code = 409, detail= f"Det finns redan ett län med id {x.id}: {x.namn}")
    return db.spara_lan(lan)

@app.put("/lan/{id}")
async def uppdatera_lan(id: int, lan: Lan) -> Lan:
    x : Optional[Lan] = db.hamta_lan(id)
    if x is None:
        raise HTTPException(status_code = 404, detail= f"Det finns inget län med id {id}.")

    if lan.id != id:
        raise HTTPException(status_code = 409, detail= f"Länets id kan inte ändras.")

    return db.spara_lan(lan)

# vattendrag


@app.get("/vattendrag")
async def lista_vattendrag() -> VattendragCollection:
    return VattendragCollection(vattendrag=db.lista_vattendrag())

@app.get("/vattendrag/{id}")
async def hamta_vattendrag_med_id(id: int) -> Vattendrag:
    vattendrag = db.hamta_vattendrag(id)
    if vattendrag is None:
        raise HTTPException(status_code=404)
    return vattendrag

@app.post("/vattendrag")
async def skapa_nytt_vattendrag(vattendrag: Vattendrag) -> Vattendrag:
    # ignorera eventuellt id i requestet
    vattendrag.id = -1
    return db.spara_vattendrag(vattendrag)

@app.put("/vattendrag/{id}")
async def uppdatera_vattendrag(id: int, vattendrag: Vattendrag) -> Vattendrag:
    x : Optional[Vattendrag] = db.hamta_vattendrag(id)
    if x is None:
        raise HTTPException(status_code = 404, detail= f"Det finns inget vattendrag med id {id}.")

    if vattendrag.id != id:
        raise HTTPException(status_code = 409, detail= f"Vattendragets id kan inte ändras.")

    return db.spara_vattendrag(vattendrag)
