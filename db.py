from typing import List, Optional

from model import *


class DummyDb():
    lan: List[Lan]
    vattendrag: List[Lan]

    def __init__(self) -> None:
        self.lan = [Lan(id=23, namn="Jämtland"),
                    Lan(id=21, namn="Gävleborg")]

        self.vattendrag = [Vattendrag(id=2,
                                      namn="Gavleån",
                                      beskrivning="Hela Gavleån är ca 2 mil lång och rinner från Storsjön till havet i Gävlebukten. Det finns 8 kraftverk på sträckan och den enda del som är intressant ur forspaddlingssynpunkt är nedströms det sista kraftverket i Boulognerskogen i centrala Gävle.",
                                      lan=[self.lanMedId(21)]
                                      ),
                           Vattendrag(id=1,
                                      namn="Testeboån",
                                      beskrivning="Ån rinner genom ett flackt skogs- och myrlandskap mellan Ockelbo och Gävle. Testeboån var tidigare flottled och spår efter detta finns kvar på sina håll.",
                                      lan=[self.lanMedId(21)]
                                      ),
                           Vattendrag(id=3,
                                      namn="Vålån",
                                      beskrivning="Vålån är en fantastisk sträcka för de som gillar brutal utförspaddling. Sträckan är 7 km med en fallhöjd av 80 m. Grad 1 - 5. Den innehåller sex svåra passager.",
                                      lan=[self.lanMedId(23)])]

    def vattendragAlla(self) -> List[Vattendrag]:
        return self.vattendrag

    def vattendragMedId(self, id: int) -> Optional[Vattendrag]:
        return next((x for x in self.vattendrag if x .id == id), None)

    def lanAlla(self) -> List[Lan]:
        return self.lan

    def lanMedId(self, id) -> Optional[Lan]:
        return next((x for x in self.lan if x.id == id), None)
