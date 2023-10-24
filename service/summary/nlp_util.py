import os

import nlpcloud

_NLP_KEY = os.environ.get("NLP_API_KEY")
_MODEL = "bart-large-cnn"
_SUMMARY_SIZE = "large"
_USE_GPU = False


_client = nlpcloud.Client(
    _MODEL,
    _NLP_KEY,
    gpu=_USE_GPU,
)


def request_summaryzation(sentence: str) -> str:
    return _client.summarization(
        sentence,
        size=_SUMMARY_SIZE,
    )["summary_text"]
