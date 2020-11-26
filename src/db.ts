import { readFileSync } from "fs"
import { load } from "js-yaml"

export function initDb(): Db {
    return new Db()
}

interface Vattendrag {
    id: number;
    namn: string;
    beskrivning: string;
}

interface Forsstracka {
    id: number;
    namn: string;
    klass: string;
    langd: number;
    fallhojd: number;
    smhi: number;
    flode: {
        min: number;
        opt: number;
        max: number;
    };
}

interface Lan {
    id: number;
    namn: string;
}

class Db {
    lanMap: Map<number, Lan> = new Map()
    vattendragMap: Map<number, Vattendrag> = new Map()
    forsstrackaMap: Map<number, Forsstracka> = new Map()

    lan(id: number): Lan | undefined {
        return this.lanMap.get(id)
    }

    vattendrag(id: number): Vattendrag | undefined {
        return this.vattendragMap.get(id)
    }

    forsstracka(id: number): Forsstracka | undefined {
        return this.forsstrackaMap.get(id)
    }

    laddaLan(filename: string): Lan {
        const lan = load(readFileSync(filename, { encoding: "utf-8" }))
        this.kollaDublett(this.lan(lan.id), lan)
        this.lanMap.set(lan.id, lan)
        return lan
    }

    laddaVattendrag(filename: string): Vattendrag {
        const vattendrag = load(readFileSync(filename, { encoding: "utf-8" }))
        this.kollaDublett(this.vattendrag(vattendrag.id), vattendrag)
        this.vattendragMap.set(vattendrag.id, vattendrag)
        return vattendrag
    }

    kollaDublett(existerande: any, nytt: any): void {
        if (existerande) {
            console.error("Duplicerat id!");
            console.error(existerande);
            console.error(nytt);
            process.exit(1)
        }
    }

    laddaForsstracka(filename: string): Forsstracka {
        const forsstracka = load(readFileSync(filename, { encoding: "utf-8" }))
        this.kollaDublett(this.forsstracka(forsstracka.id), forsstracka)

        this.forsstrackaMap.set(forsstracka.id, forsstracka)
        return forsstracka
    }
}

