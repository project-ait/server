import json
import os
from enum import StrEnum
from urllib import parse

import requests

_URL = "https://api-free.deepl.com/v2/translate"
_DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")


class LangCode(StrEnum):
    KO = "KO"
    EN = "EN"


def translate(
        text: str,
        source: LangCode | None = None,
        target: LangCode = LangCode.KO,
) -> str | None:
    headers = {
        "Authorization": f"DeepL-Auth-Key {_DEEPL_API_KEY}",
    }

    data = {
        "text": text,
        "source_lang": source,
        "target_lang": target,
    }

    res = requests.post(url=_URL, headers=headers, data=data)

    if res.status_code != 200:
        print(res)
        print(res.text)
        return None

    json_obj = json.loads(res.text)

    return parse.unquote(json_obj["translations"][0]["text"])
