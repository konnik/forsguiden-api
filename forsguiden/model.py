from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
import datetime


class Lan(BaseModel):
    id: int
    namn: str


class Vattendrag(BaseModel):
    id: int
    namn: str
    beskrivning: str
    lan: List[Lan]


class VattendragCollection(BaseModel):
    vattendrag: List[Vattendrag]


class LanCollection(BaseModel):
    lan: List[Lan]


class Grad(str, Enum):
    ett = "1"
    tva = "2"
    tre_minus = "3-"
    tre = "3"
    tre_plus = "3+"
    fyra_minus = "4-"
    fyra = "4"
    fyra_plus = "4+"
    fem_minus = "5-"
    fem = "5"
    fem_plus = "5+"
    sex = "6"


class Gradering(BaseModel):
    klass: Grad
    lyft: List[Grad]


class Position(BaseModel):
    lat: float
    long: float


class Flode(BaseModel):
    smhipunkt: int
    minimum: int
    optimal: int
    maximum: int


class ForsstrackaVattendrag(BaseModel):
    id: int
    namn: str


class ForsstrackaLan(BaseModel):
    id: int
    namn: str


class Forsstracka(BaseModel):
    id: Optional[int]
    namn: str
    gradering: Gradering
    langd: int
    fallhojd: int
    koordinater: Position
    flode: Flode
    vattendrag: List[ForsstrackaVattendrag]
    lan: List[ForsstrackaLan]


class ForsstrackaCollection(BaseModel):
    forsstracka: List[Forsstracka]


class NyForsstrackaBeskrivning(BaseModel):
    beskrivning: str


class ForsstrackaBeskrivning(BaseModel):
    beskrivning: str
    uppdaterad: datetime.datetime
    uppdaterad_av: str


class DataDump(BaseModel):
    lan: List[Lan]
    vattendrag: List[Vattendrag]
    forsstracka: List[Forsstracka]
