from typing import List, Optional
from model import *
from db import Db

class InMemoryDb(Db):
    lan: List[Lan]
    vattendrag: List[Vattendrag]
    forsstracka: List[Forsstracka]

    def __init__(self, generera_testdata = False) -> None:
        self.lan = []
        self.vattendrag = []
        self.forsstracka = []

        if generera_testdata:
            self.generera_testdata()

    # --------- Vattendrag ----------

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

    # ---------- Län ----------
    def lista_lan(self) -> List[Lan]:
        return self.lan

    def hamta_lan(self, id) -> Optional[Lan]:
        return next((x for x in self.lan if x.id == id), None)

    def spara_lan(self, nytt_lan: Lan) -> Lan:
        lan2 = [l for l in self.lan if l.id != nytt_lan.id]
        lan2.append(nytt_lan)
        self.lan = lan2
        return nytt_lan

    # ---------- Forssträcka ----------
    def lista_forsstracka(self) -> List[Forsstracka]:
        return self.forsstracka

    def hamta_forsstracka(self, id) -> Optional[Forsstracka]:
        return next((x for x in self.forsstracka if x.id == id), None)

    def spara_forsstracka(self, ny_forsstracka: Forsstracka) -> Forsstracka:
        if ny_forsstracka.id == -1:
            ny_forsstracka.id = max(x.id for x in self.forsstracka) + 1

        forsstracka2 = [x for x in self.forsstracka if x.id != ny_forsstracka.id]
        forsstracka2.append(ny_forsstracka)

        self.forsstracka = forsstracka2
        return ny_forsstracka

    # ---------- Testdata ----------
    def generera_testdata(self):
        self.spara_lan(Lan(id=21, namn="Gävleborg"))
        self.spara_lan(Lan(id=23, namn="Jämtland"))

        self.spara_vattendrag(Vattendrag(id=2,
                                      namn="Gavleån",
                                      beskrivning="Hela Gavleån är ca 2 mil lång och rinner från Storsjön till havet i Gävlebukten. Det finns 8 kraftverk på sträckan och den enda del som är intressant ur forspaddlingssynpunkt är nedströms det sista kraftverket i Boulognerskogen i centrala Gävle.",
                                      lan=[self.hamta_lan(21)]
                                      ))
                                      
        self.spara_vattendrag(Vattendrag(id=1,
                                      namn="Testeboån",
                                      beskrivning="Ån rinner genom ett flackt skogs- och myrlandskap mellan Ockelbo och Gävle. Testeboån var tidigare flottled och spår efter detta finns kvar på sina håll.",
                                      lan=[self.hamta_lan(21)]
                                      ))

        self.spara_vattendrag(Vattendrag(id=3,
                                      namn="Vålån",
                                      beskrivning="Vålån är en fantastisk sträcka för de som gillar brutal utförspaddling. Sträckan är 7 km med en fallhöjd av 80 m. Grad 1 - 5. Den innehåller sex svåra passager.",
                                      lan=[self.hamta_lan(23)]
                                      ))
        
        self.spara_forsstracka(Forsstracka(id=1,
                namn="Brännsågen-Åbyggeby",
                langd=6000,
                fallhojd=28,
                gradering=Gradering(klass=Grad.tva, lyft=[]),
                koordinater=Position(lat=60.75627, long=17.03825),
                flode = Flode(smhipunkt=12020, minimum=20, maximum=100, optimal=30),
                vattendrag=[self.hamta_vattendrag(1)],
                lan=[self.hamta_lan(21)]
                ))

        self.spara_forsstracka(Forsstracka(id=3,
                namn="Vävaren",
                gradering=Gradering(klass=Grad.tre_plus, lyft=[]),
                langd=350,
                fallhojd=12,
                koordinater=Position(lat=60.69801, long=17.15803),
                flode = Flode(smhipunkt=12020, minimum=20, maximum=40, optimal=25),
                vattendrag=[self.hamta_vattendrag(1)],
                lan=[self.hamta_lan(21)]
                ))

        self.spara_forsstracka(Forsstracka(id=4,
                namn="Konserthuset",
                gradering=Gradering(klass=Grad.tva, lyft=[]),
                langd=1000,
                fallhojd=5,
                koordinater=Position(lat=60.67298, long=17.13364),
                flode = Flode(smhipunkt=11802, minimum=30, maximum=100, optimal=60),
                vattendrag=[self.hamta_vattendrag(2)],
                lan=[self.hamta_lan(21)]
                ))
