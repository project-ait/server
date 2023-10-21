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


class ConcecutiveWeather:
    def __init__(
        self,
        hour: int,  # 시
        stat: str,  # 날씨 (한국어)
        temp: float,  # 기온
        chill: float,  # 체감온도
        rain: int,  # 강수량 (mm/h)
        pred_rain: int,  # 강수 확률 (%)
        ws: float,  # 풍속 (m/s)
        wd: str,  # 풍향 (한국어)
        reh: int,  # 습도 (%)
    ):
        self.hour = hour
        self.stat = stat
        self.temp = temp
        self.chill = chill
        self.rain = rain
        self.pred_rain = pred_rain
        self.ws = ws
        self.wd = wd
        self.reh = reh
