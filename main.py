from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from model import *
from db import DummyDb


app = FastAPI()
db = DummyDb()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# län

class LanCollection(BaseModel):
    lan: List[Lan]

@app.get("/lan")
async def lista_lan() -> LanCollection:
    return LanCollection(lan=db.lanAlla())

@app.get("/lan/{id}")
async def hamta_lan_med_id(id: int) -> Lan:
    lan = db.lanMedId(id)
    if lan is None:
        raise HTTPException(status_code=404)
    return lan

# vattendrag

class VattendragCollection(BaseModel):
    vattendrag: List[Vattendrag]

@app.get("/vattendrag")
async def lista_vattendrag() -> LanCollection:
    return VattendragCollection(vattendrag=db.vattendragAlla())

@app.get("/vattendrag/{id}")
async def hamta_vattendrag_med_id(id: int) -> Vattendrag:
    vattendrag = db.vattendragMedId(id)
    if vattendrag is None:
        raise HTTPException(status_code=404)
    return vattendrag
