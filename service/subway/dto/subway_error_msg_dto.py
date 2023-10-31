from enum import StrEnum


class SubwayErrorCode(StrEnum):
    INFO000 = "정상 처리되었습니다."
    ERROR300 = "필수 값이 누락되어 있습니다."
    INFO100 = "인증키가 유효하지 않습니다."
    ERROR301 = "파일타입 값이 누락 혹은 유효하지 않습니다."
    ERROR310 = "해당하는 서비스를 찾을 수 없습니다."
    ERROR331 = "요청시작위치 값을 확인하십시오."
    ERROR332 = "요청종료위치 값을 확인하십시오."
    ERROR333 = "요청위치 값의 타입이 유효하지 않습니다."
    ERROR334 = "요청종료위치 보다 요청시작위치가 더 큽니다."
    ERROR335 = "샘플데이터(샘플키:sample) 는 한번에 최대 5건을 넘을 수 없습니다."
    ERROR336 = "데이터요청은 한번에 최대 1000건을 넘을 수 없습니다."
    ERROR500 = "서버 오류입니다."
    ERROR600 = "데이터베이스 연결 오류입니다."
    ERROR601 = "SQL 문장 오류 입니다."
    INFO200 = "해당하는 데이터가 없습니다."


class SubwayErrorMsgDto:
    def __init__(
        self,
        status: int,
        code: SubwayErrorCode,
        message: str,
        link: str,
        dev_msg: str,
        total: int,
    ):
        self.status = status
        self.code = code
        self.message = message
        self.link = link
        self.dev_msg = dev_msg
        self.total = total

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            status=int(data["status"]),
            code=SubwayErrorCode[data["code"].replace("-", "")],
            message=data["message"],
            link=data["link"],
            dev_msg=data["developerMessage"],
            total=data["total"],
        )
