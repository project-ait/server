import json

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Request

from service.weather.dto.weather_dto import ConcecutiveWeather, DetailWeather
from service.weather.weather_location_util import find_near_dong

router = APIRouter()


@router.get("/")
def weather_detail(
    request: Request,
    lat: float | None = None,
    lon: float | None = None,
):
    if lat == None or lon == None:
        ip = request.client.host
        lat, lon = get_location(ip)
    data = find_near_dong(lat, lon)

    return get_single_weather(data.code, data.lat, data.lon)


@router.get("/list")
def weather_list(
    request: Request,
    lat: float | None = None,
    lon: float | None = None,
):
    if lat == None or lon == None:
        ip = request.client.host
        lat, lon = get_location(ip)
    data = find_near_dong(lat, lon)

    return get_concecutive_weather(data.code, data.lat, data.lon)


def get_location(ip: str) -> (float, float):
    _ipinfo_url = "https://ipinfo.io"
    _ipinfo_token = "ed776abe608c8f"
    url = "{}/{}?token={}".format(
        _ipinfo_url,
        ip,
        _ipinfo_token,
    )
    resp = json.loads(requests.get(url).text)
    loc = resp["loc"].split(",")
    return float(loc[0]), float(loc[1])


def get_single_weather(
    code: str,
    lat: float,
    lon: float,
) -> DetailWeather:
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
    minmax = temp_section.find_all("span")
    tmin = minmax[2].get_text()[:-1]
    tmin = float(tmin) if tmin.isdigit() else None
    tmax = minmax[4].get_text()[:-1]
    tmax = float(tmax) if tmax.isdigit() else None

    # TODO: 만약 체감온도가 없으면 오류발생함
    chill = float(ul[0].find("span", class_="chill").get_text()[3:-2])

    val_section = ul[1].find_all("span", class_="val")
    rain = val_section[2].get_text()[:-3]
    rain = 0 if rain == "-" else float(rain)

    reh = int(val_section[0].get_text()[:-1])

    wind = val_section[1].get_text().split(" ")
    ws = wind[1]
    wd = wind[0]

    dst_section = ul[3].find_all("span", class_="air-lvv")
    fdst = float(dst_section[1].get_text())
    ffdst = float(dst_section[0].get_text())

    return DetailWeather(
        temp=temp,
        tmin=tmin,
        tmax=tmax,
        chill=chill,
        rain=rain,
        reh=reh,
        ws=ws,
        wd=wd,
        fdst=fdst,
        ffdst=ffdst,
    )


def get_concecutive_weather(
    code: str,
    lat: float,
    lon: float,
) -> list[ConcecutiveWeather]:
    body = requests.get(
        "https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?code={}&unit=m%2Fs&hr1=Y&lat={}&lon={}".format(
            code,
            lat,
            lon,
        ),
    ).text

    soup = BeautifulSoup(body, "html.parser")

    ls = [*soup.find_all("ul", class_="vs-item"), *soup.find_all("ul", class_="s-item")]
    ls = ls[:-24]  # 마지막 24개 (글피 데이터) 삭제

    for i in range(len(ls)):
        item = ls[i].find_all("span")
        hour = int(item[1].get_text()[:-1])
        stat = item[3].get_text()
        temp = float(item[5].get_text().split("(")[0][:-1])
        chill = float(item[8].get_text()[:-1])
        rain = item[10].get_text()
        rain = 0 if rain == "-" else int(rain)
        pred_rain = item[12].get_text()[:-1]
        pred_rain = 0 if pred_rain == "" else int(pred_rain)
        ws = float(item[15].get_text()[:-3])
        wd = item[14].get_text()
        reh = int(item[18].get_text()[:-1])
        ls[i] = ConcecutiveWeather(
            hour=hour,
            stat=stat,
            temp=temp,
            chill=chill,
            rain=rain,
            pred_rain=pred_rain,
            ws=ws,
            wd=wd,
            reh=reh,
        )

    return ls
