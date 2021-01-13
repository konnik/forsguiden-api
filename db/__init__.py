from typing import List, Optional
from model import *

class Db():
    def lista_vattendrag(self) -> List[Vattendrag]:
        raise NotImplemented

    def hamta_vattendrag(self, id: int) -> Optional[Vattendrag]:
        raise NotImplemented
    
    def spara_vattendrag(self, nytt_vattendrag: Vattendrag) -> Vattendrag:
        raise NotImplemented

    def lista_lan(self) -> List[Lan]:
        raise NotImplemented

    def hamta_lan(self, id) -> Optional[Lan]:
        raise NotImplemented

    def spara_lan(self, nyttlan: Lan) -> Lan:
        raise NotImplemented


