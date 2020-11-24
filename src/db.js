const initDb = function() {
    const db = {
        lan : {}
    }

    return {
        getData: () => db,
        sparaLan: (obj) => {
            if (db[obj.id]) {
                throw "Ett län med id " + obj.id + " finns redan."
            }
            db.lan[obj.id] = obj
            return obj
        },
        sparaVattendrag: (obj) => {
            if (db.vattendrag[obj.id]) {
                throw "Ett vattendrag med id " + obj.id + " finns redan."
            }
            db.vattendrag[obj.id] = obj
            return obj
        }
    }
}

module.exports = {
    initDb: initDb
}
