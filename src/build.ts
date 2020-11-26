
import { initDb } from "./db"


const db = initDb()

const gavleborg = db.laddaLan("./data/gavleborg/data.yml");
const gavlean = db.laddaVattendrag("./data/gavleborg/gavlean/data.yml");
const testeboan = db.laddaVattendrag("./data/gavleborg/testeboan/data.yml");
const konserthuset = db.laddaForsstracka("./data/gavleborg/gavlean/konserthuset/data.yml");


console.log(gavleborg);
console.log(gavlean);
console.log(testeboan);
console.log(konserthuset)


