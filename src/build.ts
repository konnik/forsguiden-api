import { writeFileSync } from "fs"
import { initDb } from "./db"


const db = initDb()

const jamtland = db.laddaLan("./data/jamtland/data.yml");
const gavleborg = db.laddaLan("./data/gavleborg/data.yml");

const gavlean = db.laddaVattendrag("./data/gavleborg/gavlean/data.yml");
const konserthuset = db.laddaForsstracka("./data/gavleborg/gavlean/konserthuset/data.yml");

const testeboan = db.laddaVattendrag("./data/gavleborg/testeboan/data.yml");
const brannsagen = db.laddaForsstracka("./data/gavleborg/testeboan/brannsagen-abyggeby/data.yml");
const vavaren = db.laddaForsstracka("./data/gavleborg/testeboan/vavaren/data.yml");
const forsby = db.laddaForsstracka("./data/gavleborg/testeboan/forsby/data.yml");

const allData = {
    lan: [jamtland, gavleborg],
    vattendrag: [gavlean, testeboan],
    forsstrackor: [konserthuset, brannsagen, vavaren, forsby]
}

console.log(JSON.stringify(allData))
writeFileSync("./dist/data.json", JSON.stringify(allData), { encoding: "utf-8" })


