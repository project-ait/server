class NearDongDto:
    def __init__(
        self,
        code: str,
        name: str,
        short_name: str,
        x: int,
        y: int,
        lat: float,
        lon: float,
        level: int,
        name_en: str,
        short_name_en: str,
    ):
        self.code = code
        self.name = name
        self.short_name = short_name
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon
        self.level = level
        self.name_en = name_en
        self.short_name_en = short_name_en
