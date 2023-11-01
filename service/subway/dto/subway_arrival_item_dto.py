from enum import Enum
from typing import List


class SubwayId(str, Enum):
    s1001 = "1호선"
    s1002 = "2호선"
    s1003 = "3호선"
    s1004 = "4호선"
    s1005 = "5호선"
    s1006 = "6호선"
    s1007 = "7호선"
    s1008 = "8호선"
    s1009 = "9호선"
    s1061 = "중앙선"
    s1063 = "경의중앙선"
    s1065 = "공항철도"
    s1067 = "경춘선"
    s1075 = "수의분당선"
    s1077 = "신분당선"
    s1092 = "우이신설선"
    s1093 = "서해선"
    s1081 = "경강선"


class ArrivalCode(str, Enum):
    a0 = "진입"
    a1 = "도착"
    a2 = "출발"
    a3 = "전역출발"
    a4 = "전역진입"
    a5 = "전역도착"
    a99 = "운행중"


class SubwayArrivalItemDto:
    def __init__(
        self,
        subway_id: SubwayId,  # 지하철 호선 ID (1호선, 3호선, 경춘선 등)
        up_down_line: str,  # (상행, 하행)
        train_line_name: str,  #  종착지 - 다음역
        prev_station_id: str,  # 이전역 id
        next_station_id: str,  # 다음역 id
        station_id: str,  # 역 id
        station_name: str,  # 역 이름
        trnsitCo: int,  # 환승 노선 수
        # ord_key 는 필요없다 판단되어 추가 안함
        subway_list: List[SubwayId],  # 연계 호선 Id
        station_list: List[str],  # 연계 지하철역 Id
        train_type: str,  # 급행, 일반 등의 열차 종류
        pred_sec: int,  # 예상 도착 시간 (초)
        train_no: int,  # 열차번호
        station_end_id: int,  # 종착역 id
        station_end_name: str,  # 종착역 이름
        generated_date: str,  # 도착정보를 생성한 시각
        arrival_msg_2: str,  # 첫 번째 도착 메세지 (도착, 출발, 진입 등)
        arrival_msg_3: str,  # 두 번재 도착 메세지 (종합운동장 도착, 12분 후 등)
        arrival_code: ArrivalCode,  # 도착 코드
    ):
        self.subway_id = subway_id
        self.up_down_line = up_down_line
        self.train_line_name = train_line_name
        self.prev_station_id = prev_station_id
        self.next_station_id = next_station_id
        self.station_id = station_id
        self.station_name = station_name
        self.trnsitCo = trnsitCo
        self.subway_list = subway_list
        self.station_list = station_list
        self.train_type = train_type
        self.pred_sec = pred_sec
        self.train_no = train_no
        self.station_end_id = station_end_id
        self.station_end_name = station_end_name
        self.generated_date = generated_date
        self.arrival_msg_2 = arrival_msg_2
        self.arrival_msg_3 = arrival_msg_3
        self.arrival_code = arrival_code

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            subway_id=SubwayId["s" + data["subwayId"]],
            up_down_line=data["updnLine"],
            train_line_name=data["trainLineNm"],
            prev_station_id=data["statnFid"],
            next_station_id=data["statnTid"],
            station_id=data["statnId"],
            station_name=data["statnNm"],
            trnsitCo=int(data["trnsitCo"]),
            subway_list=[SubwayId["s" + e] for e in data["subwayList"].split(",")],
            station_list=data["statnList"],
            train_type=data["btrainSttus"],
            pred_sec=int(data["barvlDt"]),
            train_no=data["btrainNo"],
            station_end_id=data["bstatnId"],
            station_end_name=data["bstatnNm"],
            generated_date=data["recptnDt"],
            arrival_msg_2=data["arvlMsg2"],
            arrival_msg_3=data["arvlMsg3"],
            arrival_code=ArrivalCode["a" + data["arvlCd"]],
        )
