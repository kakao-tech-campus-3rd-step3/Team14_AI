from typing import Optional, Literal
from datetime import date
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class FestivalOut(BaseModel):
    id: int
    areaCode: int
    endDate: date
    startDate: date
    manager_id: Optional[int]
    homePage: Optional[str]
    overView: str
    addr1: str
    addr2: Optional[str]
    contentId: Optional[str]
    posterInfo: str
    title: str
    state: Literal["APPROVED", "DENIED", "PROCESSING"]

    class Config:
        from_attributes = True

# 1) 축제 스타일(복수 선택)
FestivalStyle = Literal[
    "전통문화", "예술/공연", "먹거리",
    "자연/경관", "체험/참여", "트렌디",
    "커뮤니티", "지역특색", "국제"
]

# 2) 여행 MBTI (각 문항 1개 선택)
class TravelMBTI(BaseModel):
    place_preference: Literal["새로운 곳", "익숙한 곳"]
    companionship:    Literal["혼자서", "친구들과"]
    focus:            Literal["즐거움", "유익함"]
    planning_style:   Literal["즉흥적으로", "계획적으로"]

# 3) 전체 입력 페이로드
class PreferenceIn(BaseModel):
    festival_styles: List[FestivalStyle] = Field(..., min_length=1, description="축제 스타일 최소 1개 이상")
    travel_mbti: TravelMBTI
    additional_notes: Optional[str] = Field(None, max_length=500, description="자유기입(최대 500자)")

# 응답(테스트용 에코)
class PreferenceAck(BaseModel):
    ok: bool
    selected_styles: List[FestivalStyle]
    mbti: TravelMBTI
    notes: Optional[str]
