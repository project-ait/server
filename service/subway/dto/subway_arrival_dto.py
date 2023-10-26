from typing import List

from service.subway.dto.subway_arrival_item_dto import SubwayArrivalItemDto
from service.subway.dto.subway_error_msg_dto import SubwayErrorMsgDto


class SubwayArrivalDto:
    def __init__(
        self,
        error_msg: SubwayErrorMsgDto,
        items: List[SubwayArrivalItemDto],
    ):
        self.error_msg = error_msg
        self.items = items

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            error_msg=SubwayErrorMsgDto.from_json(data["errorMessage"]),
            items=[
                SubwayArrivalItemDto.from_json(e) for e in data["realtimeArrivalList"]
            ],
        )
