import re

from transformers import pipeline

_MIN_LENGTH = 30
_TASK = "summarization"
_MODEL = "facebook/bart-large-cnn"


_client = pipeline(
    task=_TASK,
    model=_MODEL,
)


def bart_summaryzation(sentence: str) -> str:
    # 문서에 파라미터 언급 없음, max-length 는 토큰 수로 추정되는데
    # 이를 계산하기 위해서는 귀찮은 방벙이 필요함으로
    # AI답게, 그냥 대충 비슷한 숫자가 되게끔 임의로 맞춤
    return _client(
        sentence,
        max_length=max(re.split("\s", sentence), _MIN_LENGTH),
        min_length=_MIN_LENGTH,
    )
