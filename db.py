from typing import List, Optional

from model import *


class DummyDb():
    lan: List[Lan]
    vattendrag: List[Vattendrag]

    def __init__(self) -> None:
        self.lan = [Lan(id=23, namn="Jämtland"),
                    Lan(id=21, namn="Gävleborg")]

        self.vattendrag = [Vattendrag(id=2,
                                      namn="Gavleån",
                                      beskrivning="Hela Gavleån är ca 2 mil lång och rinner från Storsjön till havet i Gävlebukten. Det finns 8 kraftverk på sträckan och den enda del som är intressant ur forspaddlingssynpunkt är nedströms det sista kraftverket i Boulognerskogen i centrala Gävle.",
                                      lan=[self.hamta_lan(21)]
                                      ),
                           Vattendrag(id=1,
                                      namn="Testeboån",
                                      beskrivning="Ån rinner genom ett flackt skogs- och myrlandskap mellan Ockelbo och Gävle. Testeboån var tidigare flottled och spår efter detta finns kvar på sina håll.",
                                      lan=[self.hamta_lan(21)]
                                      ),
                           Vattendrag(id=3,
                                      namn="Vålån",
                                      beskrivning="Vålån är en fantastisk sträcka för de som gillar brutal utförspaddling. Sträckan är 7 km med en fallhöjd av 80 m. Grad 1 - 5. Den innehåller sex svåra passager.",
                                      lan=[self.hamta_lan(23)])]

    def lista_vattendrag(self) -> List[Vattendrag]:
        return self.vattendrag

    def hamta_vattendrag(self, id: int) -> Optional[Vattendrag]:
        return next((x for x in self.vattendrag if x .id == id), None)
    
    def spara_vattendrag(self, nytt_vattendrag: Vattendrag) -> Vattendrag:
        if nytt_vattendrag.id == -1:
            nytt_vattendrag.id = max(x.id for x in self.vattendrag) + 1

        vattendrag2 = [x for x in self.vattendrag if x.id != nytt_vattendrag.id]
        vattendrag2.append(nytt_vattendrag)

        self.vattendrag = vattendrag2
        return nytt_vattendrag

    def lista_lan(self) -> List[Lan]:
        return self.lan

    def hamta_lan(self, id) -> Optional[Lan]:
        return next((x for x in self.lan if x.id == id), None)

    def spara_lan(self, nyttlan: Lan) -> Lan:
        lan2 = [l for l in self.lan if l.id != nyttlan.id]
        lan2.append(nyttlan)
        self.lan = lan2
        return nyttlan
