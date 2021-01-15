from typing import List, Optional
from forsguiden.model import *


class Db:
    # Vattendrag
    def lista_vattendrag(self) -> List[Vattendrag]:
        raise NotImplemented

    def hamta_vattendrag(self, id: int) -> Optional[Vattendrag]:
        raise NotImplemented

    def spara_vattendrag(self, nytt_vattendrag: Vattendrag) -> Vattendrag:
        raise NotImplemented

    def radera_vattendrag(self, id: int) -> bool:
        raise NotImplemented

    # Län
    def lista_lan(self) -> List[Lan]:
        raise NotImplemented

    def hamta_lan(self, id) -> Optional[Lan]:
        raise NotImplemented

    def spara_lan(self, nytt_lan: Lan) -> Lan:
        raise NotImplemented

    def radera_lan(self, id) -> bool:
        raise NotImplemented

    # Forssträcka
    def lista_forsstracka(self) -> List[Forsstracka]:
        raise NotImplemented

    def hamta_forsstracka(self, id: int) -> Optional[Forsstracka]:
        raise NotImplemented

    def spara_forsstracka(self, ny_forsstracka: Forsstracka) -> Forsstracka:
        raise NotImplemented

    def radera_forsstracka(self, id: int) -> bool:
        raise NotImplemented
