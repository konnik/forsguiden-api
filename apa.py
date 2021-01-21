import os
import psycopg2
import dotenv
from forsguiden.db.postgres import PostgresDb
from forsguiden.model import *

dotenv.load_dotenv()
db = PostgresDb(psycopg2.connect(os.environ["DATABASE_URL"]))

f = Forsstracka(
    id=-1,
    namn="Brännsågen-Åbyggeby",
    langd=6000,
    fallhojd=28,
    gradering=Gradering(klass=Grad.tva, lyft=[Grad.tre_plus, Grad.fyra_minus]),
    koordinater=Position(lat=60.75627, long=17.03825),
    flode=Flode(smhipunkt=12020, minimum=20, maximum=100, optimal=30),
    vattendrag=[ForsstrackaVattendrag(id=1, namn="Testeboån")],
    lan=[ForsstrackaLan(id=21, namn="Gävleborg")],
)

print(db.spara_forsstracka(f))