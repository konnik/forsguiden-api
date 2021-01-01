import { split } from "ts-node"

export interface Lan {
    id: number;
    namn: string;
}

export interface Vattendrag {
    id: number;
    namn: string;
    beskrivning: string;
}

export type Grad = "1" | "1+" | "2-" | "2" | "2+" | "3-" | "3" | "3+" | "4-" | "4" | "4+" | "5-" | "5" | "5+" | "6"

export type Gradering = {
    klass: Grad;
    lyft: Grad[];
}

export function graderingFromString(value:string): Gradering {
    val parts = split(value)    

    return {
        klass: parts[0]
    }
}


export interface Forsstracka {
    id: number;
    namn: string;
    gradering: Gradering;
    langd: number;
    fallhojd: number;
    flode: {
        smhiPunkt: number;
        min: number;
        opt: number;
        max: number;
    };
}


