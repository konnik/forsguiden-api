const fs = require("fs")
const path = require("path")
const glob = require("glob");
const yaml = require("js-yaml");

const allaLan = glob.sync("data/*")

for (const lanFolder of allaLan) {
    console.log("Län: ", lanFolder)
    const lanData = yaml.load(fs.readFileSync(lanFolder + "/data.yml", { encoding: "utf-8" }))
    console.log(JSON.stringify(lanData))
}

