import shutil
from enum import Enum
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from core.response import Response, ResponseStatus
# from service.summary.bart_util import generate_summary
from service.deepl import LangCode, translate
from service.summary.nlp_util import text_summary
from service.summary.stt.whisper_util import speech_to_text

_MIN_TEXT_LEN = 100

router = APIRouter()


@router.post("/")
def summary(audio_file: UploadFile):
    # with 를 통해 임시파일을 자동으로 지울 경우 알 수 없는 원인의 permission 오류 발생,
    # 따라서 수동으로 진행
    tmp_file = NamedTemporaryFile(delete=False)
    shutil.copyfileobj(audio_file.file, tmp_file)

    # 파일을 읽어 텍스트 데이터로 변환 AI
    stt = speech_to_text(tmp_file.name)
    tmp_file.close()

    if stt is None:
        return Response(
            ResponseStatus.fail,
            {"code": SummaryResponseCode.FILE_CANNOT_READ.name},
        )
    if len(stt) < _MIN_TEXT_LEN:
        return Response(
            ResponseStatus.fail,
            {
                "code": SummaryResponseCode.FILE_LENGTH_TOO_SHORT.name,
                "text": stt,
            },
        )

    # 내용 요약 모델을 위해 한국어를 영어로 번역
    translated_en = translate(stt, source=LangCode.KO, target=LangCode.EN)
    if translated_en is None:
        return Response(
            ResponseStatus.fail,
            {"code": SummaryResponseCode.SERVICE_NOT_AVAILABLE.name},
        )

    # NLP 혹은 BART 모델을 이용해 내용 요약
    summarized_model = "NLP"
    summarized = text_summary(translated_en)
    # if summarized == None:
    #     summarized = generate_summary(translated_en)
    #     summarized_model = "bart"

    # 사용자에게 전달하기 위해 영어 요약 내용을 한국어로 번역
    translated_ko = translate(
        summarized, source=LangCode.EN, target=LangCode.KO
    )
    if translated_ko is None:
        return Response(
            ResponseStatus.fail,
            {"code": SummaryResponseCode.SERVICE_NOT_AVAILABLE.name},
        )

    return Response(
        ResponseStatus.success,
        {
            "text": translated_ko,
            "model_name": summarized_model,
        },
    )


class SummaryResponseCode(Enum):
    FILE_CANNOT_READ = 0  # 파일을 읽을 수 없을 때 (형식, 파일깨짐, 코덱없음 등)
    FILE_LENGTH_TOO_SHORT = 1  # 대화 내용을 텍스트로 변환했을 때, 길이가 짧아 요약이 불가능
    SERVICE_NOT_AVAILABLE = 2  # API 사용량 초과로 사용 불가능
