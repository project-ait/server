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
        error_msg = data["errorMessage"]
        return cls(
            error_msg=SubwayErrorMsgDto.from_json(
                error_msg if error_msg is not None else data
            ),
            items=[
                SubwayArrivalItemDto.from_json(e) for e in data["realtimeArrivalList"]
            ]
            if error_msg is not None
            else [],
        )
