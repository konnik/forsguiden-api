const glob = require("glob");
const util = require("./util")
const db = require("./db").initDb()

const allaLan = glob.sync("data/*")

for (const lanFolder of allaLan) {
    console.log("Län: ", lanFolder)

    const lanData = db.sparaLan(util.laddaObjekt(lanFolder + "/data.yml"))

    console.log(JSON.stringify(lanData))

    Object.keys(lanData).forEach( k => console.log(k + "=>" + lanData[k]))
}

