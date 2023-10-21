import json

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Request

from service.weather.dto.near_dong_dto import NearDongDto
from service.weather.dto.weather_dto import DetailWeather
from service.weather.weather_location_util import find_near_dong

router = APIRouter()

# 날씨정보 시계열, lat lon 쿼리파라미터 추가
# https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?code=1114060500&unit=m%2Fs&hr1=Y&lat=37.5682&lon=126.9977


@router.get("/")
def python(request: Request, lat: float | None = None, lon: float | None = None):
    ip = request.client.host
    if lat == None or lon == None:
        lat, lon = get_location(ip)
    data: NearDongDto = find_near_dong(lat, lon)

    return get_single_weather(data.code, data.lat, data.lon)


def get_location(ip: str) -> (float, float):
    _ipinfo_url = "https://ipinfo.io"
    _ipinfo_token = "ed776abe608c8f"
    url = "{}/{}?token={}".format(
        _ipinfo_url,
        ip,
        _ipinfo_token,
    )
    resp = json.loads(requests.get(url).text)
    print(resp)
    loc = resp["loc"].split(",")
    return float(loc[0]), float(loc[1])


def get_single_weather(code: str, lat: float, lon: float) -> DetailWeather:
    body = requests.get(
        "https://www.weather.go.kr/w/wnuri-fct2021/main/current-weather.do?&unit=m%2Fs*code={}&aws=N&lat={}&loc={}".format(
            code,
            lat,
            lon,
        )
    ).text
    soup = BeautifulSoup(body, "html.parser")

    ul = soup.find_all("ul")

    temp_section = ul[0].find("span", class_="tmp")
    temp = float(temp_section.get_text().split("℃")[0])
    minmax: str = temp_section.find_all("span")
    tmin = minmax[2].get_text()[:-1]
    tmin = float(tmin) if tmin.isdigit() else None
    tmax = minmax[4].get_text()[:-1]
    tmax = float(tmax) if tmax.isdigit() else None

    # TODO: 만약 체감온도가 없으면 오류발생함
    chill = float(ul[0].find("span", class_="chill").get_text()[3:-2])

    val_section = ul[1].find_all("span", class_="val")
    rain = val_section[2].get_text()[:-3]
    rain = None if rain == "-" else float(rain)

    reh = int(val_section[0].get_text()[:-1])

    wind = val_section[1].get_text().split(" ")
    ws = wind[1]
    wd = wind[0]

    dst_section = ul[3].find_all("span", class_="air-lvv")
    fdst = float(dst_section[1].get_text())
    ffdst = float(dst_section[0].get_text())

    return DetailWeather(
        temp,
        tmin,
        tmax,
        chill,
        rain,
        reh,
        ws,
        wd,
        fdst,
        ffdst,
    )
