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
    "TRADITIONAL", "ART_PERFORMANCE", "FOOD",
    "NATURE", "EXPERIENCE", "TRENDY",
    "COMMUNITY", "LOCAL", "INTERNATIONAL"
]

# 2) 여행 MBTI (각 문항 1개 선택)
class TravelMBTI(BaseModel):
    place_preference: bool
    companionship:    bool
    focus:            bool
    planning_style:   bool

# 3) 전체 입력 페이로드
class PreferenceIn(BaseModel):
    festival_styles: List[FestivalStyle] = Field(..., min_length=1, description="축제 스타일 최소 1개 이상")
    travel_mbti: TravelMBTI
    additional_notes: Optional[str] = Field(None, max_length=500, description="자유기입(최대 500자)")

# 응답(테스트용 에코)
class PreferenceAck(BaseModel):
    ok: bool
    areaCode: int
    selected_styles: List[FestivalStyle]
    mbti: TravelMBTI
    notes: Optional[str]
