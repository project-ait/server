import os

import ipinfo

handler = ipinfo.getHandler(os.getenv("IPINFO_KEY"))


def get_location(address: str) -> (float, float):
    if address == "localhost" or address == "127.0.0.1":
        return 36.5284, 127.1711
    loc = str(handler.getDetails(address).loc)  # "36.4556,127.1247"
    loc = loc.split(",")
    return float(loc[0]), float(loc[1])
