import json
import os
import typing
from enum import StrEnum
from urllib import parse

import requests

_URL = "https://api-free.deepl.com/v2/translate"
_DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")


class LangCode(StrEnum):
    KO = "KO"
    EN = "EN"


def request_translate(
    sentence: str,
    source: LangCode,
    target: LangCode,
) -> typing.Union[str, None]:
    data = {
        "text": sentence,
        "source_lang": source,
        "target_lang": target,
    }
    headers = {
        "Authorization": f"DeepL-Auth-Key {_DEEPL_API_KEY}",
    }
    response = requests.post(url=_URL, headers=headers, data=data)

    if response.status_code != 200:
        print("error")
        print(response)
        print(response.text)
        return None

    json_obj = json.loads(response.text)
    print(json_obj)
    return parse.unquote(json_obj["translations"][0]["text"])
