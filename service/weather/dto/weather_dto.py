import typing


class DetailWeather:
    def __init__(
        self,
        temp: float,  # 기온
        tmin: typing.Union[float, None],  # 최저온도
        tmax: typing.Union[float, None],  # 최고온도
        chill: float,  # 체감온도
        rain: typing.Union[int, None],  # 강수량 (mm/h)
        reh: int,  # 습도 (%)
        ws: float,  # 풍속 (m/s)
        wd: str,  # 풍향 (한국어)
        fdst: int,  # 미세먼지 (ug/m)
        ffdst: int,  # 초미세먼지 (ug/m)
    ):
        self.temp = temp
        self.tmin = tmin
        self.tmax = tmax
        self.chill = chill
        self.rain = rain
        self.reh = reh
        self.ws = ws
        self.wd = wd
        self.fdst = fdst
        self.ffdst = ffdst
