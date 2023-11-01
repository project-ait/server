import json
import os

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Request

from service.location import get_location
from service.weather.dto.weather_dto import WeatherData, WeatherDetail
from service.weather.weather_location_util import find_near_dong

_IPINFO_URL = "https://ipinfo.io"
_IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN")

_WEATHER_IMG_COOKIE_URL = "https://m.search.daum.net/search?w=tot&"
_WEATHER_IMG_RESULT_URL = (
    "https://m.search.daum.net/qsearch?w=weather&m=balloon&viewtype=json&"
)

_SINGLE_WEATHER_DATA_URL = "https://www.weather.go.kr/w/wnuri-fct2021/main/current-weather.do?&unit=m%2Fs&aws=N"
_WEATHER_DATA_LIST_URL = "https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?unit=m%2Fs&hr1=Y"

router = APIRouter()


@router.get("/dong")
def dong(request: Request):
    data = find_near_dong(*get_location(request.client.host))
    return data


@router.get("/")
def weather_detail(
        request: Request,
        lat: float | None = None,
        lon: float | None = None,
):
    if lat is None or lon is None:
        ip = request.client.host
        lat, lon = get_location(ip)
    data = find_near_dong(lat, lon)
    if data is None:
        return dict()
    return get_single_weather(data.code, data.lat, data.lon)


@router.get("/list")
def weather_list(
        request: Request,
        lat: float | None = None,
        lon: float | None = None,
):
    if lat is None or lon is None:
        ip = request.client.host
        lat, lon = get_location(ip)
    data = find_near_dong(lat, lon)
    if data is None:
        return list()
    return get_weather_data(data.code, data.lat, data.lon)


@router.get("/image")
def weather_picture(
        request: Request,
        locate: str | None = None,
) -> str | None:
    uk = "Xo5bJRh7ab1BvzuXlkfaagAAALY"

    if locate is None:
        lat, lon = get_location(request.client.host)
        location_data = find_near_dong(lat, lon)
        locate = location_data.name

    conn1 = requests.get(
        _WEATHER_IMG_COOKIE_URL + "q={} 날씨".format(locate),
        cookies={"uvkey": uk},
        headers={"User-Agent": "virtualSite.com"},
    ).text

    try:
        mk = conn1.split('var mk = "')[1].split('"')[0]
        id = conn1.split('"id":"')[1].split('"')[0]
        code = conn1.split('"lcode":"')[1].split('"')[0]
    except Exception as e:  # what exception wtf
        print("Error while getting weather the image")
        print(e)
        # 검색 후 필요한 데이터를 가져오는데 실패
        # (부정확한 지역명, 지원하지 않는 지역 등)
        return None

    res = requests.get(
        _WEATHER_IMG_RESULT_URL
        + "mk={}&uk={}&q={}&lcode={}&id={}".format(
            mk,
            uk,
            locate,
            code,
            id,
        ),
        cookies={"uvkey": uk},
        headers={"User-Agent": "virtualSite.com"},
    )

    return json.loads(res.text)["RESULT"]["WEATHER_BALLOON"]["result"]


def get_single_weather(
        code: str,
        lat: float,
        lon: float,
) -> WeatherDetail:
    body = requests.get(
        _SINGLE_WEATHER_DATA_URL
        + f"&code={code}&lat={lat}&loc={lon}"
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

    return WeatherDetail(
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


def get_weather_data(
        code: str,
        lat: float,
        lon: float,
) -> list[WeatherData]:
    body = requests.get(
        _WEATHER_DATA_LIST_URL
        + "&code={}&lat={}&lon={}".format(
            code,
            lat,
            lon,
        )
    ).text

    soup = BeautifulSoup(body, "html.parser")

    ls = [*soup.find_all("ul", class_="vs-item"), *soup.find_all("ul", class_="s-item")]
    ls = ls[:-24]  # 마지막 24개 (글피 데이터) 삭제

    for i in range(len(ls)):
        # noinspection PyUnresolvedReferences
        item = ls[i].find_all("span")
        hour = int(item[1].get_text()[:-1])
        stat = item[3].get_text()
        temp = float(item[5].get_text().split("(")[0][:-1])
        chill = float(item[8].get_text()[:-1])
        rain = item[10].get_text()

        if rain == "-":
            rain = 0
        else:
            rain = int(rain[:-2])
            del item[12]

        pred_rain = item[12].get_text()[:-1]
        pred_rain = 0 if pred_rain == "" else int(pred_rain)
        ws = float(item[15].get_text()[:-3])
        wd = item[14].get_text()

        if ws == 0:  # 풍속이 0이면 '바람없음풍' 으로 출력되는 오류 수정
            wd = wd[:-1]
        reh = int(item[18].get_text()[:-1])
        ls[i] = WeatherData(
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
