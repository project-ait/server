import os
import typing

import nlpcloud
from nlpcloud import Client

_NLP_KEY = os.environ.get("NLP_API_KEY")
_MODEL = "bart-large-cnn"
_SUMMARY_SIZE = "small"
_USE_GPU = False

if _NLP_KEY is None:
    print("NLP_API_KEY is None! You need to using after update_nlp_client()")

_client: Client | None = None


def text_summary(sentence: str) -> typing.Union[str, None]:
    try:
        return _client.summarization(
            sentence,
            size=_SUMMARY_SIZE,
        )["summary_text"]
    except Exception as e:
        print(e)
        return None


def update_nlp_client():
    global _NLP_KEY, _client
    _NLP_KEY = os.environ.get("NLP_API_KEY")
    _client = nlpcloud.Client(
        _MODEL,
        _NLP_KEY,
        gpu=_USE_GPU,
    )
