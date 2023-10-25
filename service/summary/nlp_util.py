import typing
import os

import nlpcloud

_NLP_KEY = os.environ.get("NLP_API_KEY")
_MODEL = "bart-large-cnn"
_SUMMARY_SIZE = "small"
_USE_GPU = False


_client = nlpcloud.Client(
    _MODEL,
    _NLP_KEY,
    gpu=_USE_GPU,
)


def request_nlp_summaryzation(sentence: str) -> typing.Union[str, None]:
    try:
        return _client.summarization(
            sentence,
            size=_SUMMARY_SIZE,
        )["summary_text"]
    except Exception as e:
        print(e)
        return None
