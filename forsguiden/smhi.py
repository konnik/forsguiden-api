from urllib.request import urlopen
import urllib.error
import json
from typing import Optional
from pydantic import BaseModel


class Smhipunkt(BaseModel):
    poi: int
    poiCenter: list[float]
    nearestDownstreamStation: int


def sok_smhipunkt(x: float, y: float) -> Optional[Smhipunkt]:
    # https://vattenwebb.smhi.se/hydronu/data/point?x=577050.6352558124&y=6760575.570486804
    # json_url = urlopen(f"https://vattenwebb.smhi.se/hydronu/data/point?x={x}&y={y}")

    try:
        json_url = urlopen(f"https://vattenwebb.smhi.se/hydronu/data/point?x={x}&y={y}")
        smhi_json = json.loads(json_url.read())
        return Smhipunkt(**smhi_json)
    except urllib.error.HTTPError as e:

        if e.code == 404:
            return None
        raise e
