
import { initDb } from "./db"


const db = initDb()

const gavleborg = db.laddaLan("./data/gavleborg/data.yml");

const gavlean = db.laddaVattendrag("./data/gavleborg/gavlean/data.yml");
const konserthuset = db.laddaForsstracka("./data/gavleborg/gavlean/konserthuset/data.yml");

const testeboan = db.laddaVattendrag("./data/gavleborg/testeboan/data.yml");
const brannsagen = db.laddaForsstracka("./data/gavleborg/testeboan/brannsagen-abyggeby/data.yml");
const vavaren = db.laddaForsstracka("./data/gavleborg/testeboan/vavaren/data.yml");
const forsby = db.laddaForsstracka("./data/gavleborg/testeboan/forsby/data.yml");

console.log(gavleborg);
console.log(gavlean);
console.log(konserthuset)
console.log(testeboan);
console.log(brannsagen);
console.log(vavaren);
console.log(forsby);


