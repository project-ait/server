import json
from urllib import parse
import os
import typing
from enum import StrEnum

from core.logger import Logger
import requests

_URL = "https://api-free.deepl.com/v2/translate"
_DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")


_logger = Logger("deepl.py")


class LangCode(StrEnum):
    KO = "KO"
    EN = "EN-US"


def request_translate(
    sentence: str,
    source: LangCode,
    target: LangCode,
) -> typing.Union[str, None]:
    sentence = parse.quote(sentence)
    data = {
        "text": sentence,
        "source_lang": source.value,
        "target_lang": target.value,
    }
    headers = {
        "Authorization": f"DeepL-Auth-Key {_DEEPL_API_KEY}",
    }
    response = requests.post(url=_URL, headers=headers, data=data)
    if response.status_code != 200:
        return None
    json_obj = json.loads(response.text)
    return parse.unquote(json_obj["translations"][0]["text"])
