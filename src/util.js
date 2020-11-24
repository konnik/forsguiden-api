const fs = require("fs")
const yaml = require("js-yaml")


const laddaObjekt = function(filename) {
    return yaml.load(fs.readFileSync(filename, { encoding: "utf-8" }))
}

module.exports = {
    laddaObjekt: laddaObjekt    
}