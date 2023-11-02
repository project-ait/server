import json
import os

import requests
from fastapi import APIRouter

from service.subway.dto.subway_arrival_dto import SubwayArrivalDto

_URL = "http://swopenapi.seoul.go.kr/api/subway"
_API_KEY = os.environ.get("SUBWAY_API_KEY")
_DATA_TYPE = "json"
_SERVICE = "realtimeStationArrival"
_DATA_COUNT = "20"


router = APIRouter()


@router.get("/")
def request_subway_data(station_name: str):
    response = requests.get(
        "{}/{}/{}/{}/{}/{}/{}".format(
            _URL,
            _API_KEY,
            _DATA_TYPE,
            _SERVICE,
            0,
            _DATA_COUNT,
            station_name,
        )
    )
    try:
        data = SubwayArrivalDto.from_json(json.loads(response.text))
        data.items.sort(key=lambda x: x.pred_sec)
        return data
    except Exception as e:
        print(F"역을 찾을 수 없습니다: {e}")
        return None
