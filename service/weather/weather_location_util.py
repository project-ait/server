import json
import typing
import math

import requests

from service.weather.dto.near_dong_dto import NearDongDto


def dfs_xy_conv(lat: float, lon: float) -> (int, int):  #
    # LCC DFS 좌표변환을 위한 기초 자료
    #
    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0  # 격자 간격(km)
    SLAT1 = 30.0  # 투영 위도1(degree)
    SLAT2 = 60.0  # 투영 위도2(degree)
    OLON = 126.0  # 기준점 경도(degree)
    OLAT = 38.0  # 기준점 위도(degree)
    XO = 43  # 기준점 X좌표(GRID)
    YO = 136  # 기1준점 Y좌표(GRID)

    DEGRAD = math.pi / 180
    RADDEG = 180 / math.pi

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    rs = {}

    # to xy convert
    rs["lat"] = lat
    rs["lng"] = lon
    ra = math.tan(math.pi * 0.25 + (lat) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn
    rs["x"] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs["y"] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

    return rs


def find_near_dong(lat: float, lon: float) -> typing.Union[NearDongDto, None]:
    url = "https://www.weather.go.kr/w/rest/zone/find/dong.do"
    xy = dfs_xy_conv(lat, lon)
    data = {
        "x": xy["x"],
        "y": xy["y"],
        "lat": lat,
        "lon": lon,
        "lang": "kor",
    }

    response = requests.get(url, data=data).text[1:-1]
    if response == "":
        return None
    return NearDongDto(*(json.loads(response).values()))
