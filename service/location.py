import os

import ipinfo

handler = ipinfo.getHandlerAsync(os.getenv("IPINFO_KEY"))


async def get_location(address: str) -> (float, float):
    if address == "localhost" or address == "127.0.0.1":  # more specific
        address = "61.108.105.98"

    try:
        details = (await handler.getDetails(address)).details

        loc = details["loc"].split(",")

        return float(loc[0]), float(loc[1])
    except Exception as e:
        print(e)
        return -1, -1
