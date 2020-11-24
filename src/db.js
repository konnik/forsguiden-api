const initDb = function() {
    const db = {
        lanIds: {},
        lan : [],
        vattendragIds: {},
        vattendrag: []
    }

    return {
        getData: () => db,
        sparaLan: (obj) => {
            if (db.lanIds[obj.id]) {
                console.error("Ett län med id " + obj.id + " finns redan.")
                process.exit(1)
            }
            db.lanIds[obj.id] = obj
            db.lan.push(obj)

            return obj
        },
        sparaVattendrag: (obj) => {
            if (db.vattendragIds[obj.id]) {
                console.error("Ett vattendrag med id " + obj.id + " finns redan.")
                process.exit(1)
            }
            db.vattendragIds[obj.id] = obj
            db.vattendrag.push(obj)
            return obj
        }
    }
}

module.exports = {
    initDb: initDb
}
