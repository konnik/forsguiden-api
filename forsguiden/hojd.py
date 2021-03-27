from urllib.request import urlopen
import urllib.error
import json
from typing import Optional
from pydantic import BaseModel
import uuid


class Hojd(BaseModel):
    hojd: float


def hamta_hojd(east: float, north: float) -> Optional[Hojd]:
    transactionId: uuid.UUID = uuid.uuid1()
    try:
        json_url = urlopen(
            f" https://minkarta.lantmateriet.se/api/positionsinformation/positionsinformation/v1?transactionId={transactionId}&east={east}&north={north}"
        )
        result = json.loads(json_url.read())
        return Hojd(hojd=result["hojd"])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise e
