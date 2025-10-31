# app/schemas.py
from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import date

# ====== 공통 출력: DB Festival ======
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

FestivalStyle = Literal[
    "TRADITIONAL", "ART_PERFORMANCE", "FOOD",
    "NATURE", "EXPERIENCE", "TRENDY",
    "COMMUNITY", "LOCAL", "INTERNATIONAL"
]

InputStyle = Literal[
    "TRADITIONAL", "ART_PERFORMANCE", "FOOD",
    "NATURE", "EXPERIENCE", "TRENDY",
    "COMMUNITY", "LOCAL", "INTERNATIONAL",
    "PHOTOSHOT", "RESTING", "ACTIVITY", "CITY", "KNOWNPLACE", "FUNEXPERIENCE"  # ✅ 추가
]

# ====== 설문 입력 ======
class PreferenceIn(BaseModel):
    areaCode: int
    styles: List[InputStyle] = Field(..., min_items=1, description="공식 9개 + 확장 키워드 허용")
    isNewPlace: bool
    isSolo: bool
    prefersEnjoyment: bool
    isSpontaneous: bool
    additionalInfo: Optional[str] = None
    limit: int = Field(5, ge=1, le=50)

    # 대문자/중복 정리
    @field_validator("styles")
    @classmethod
    def normalize_styles(cls, v: List[str]) -> List[str]:
        seen = {}
        for s in v:
            s_up = s.upper().strip()
            seen[s_up] = True
        return list(seen.keys())

# ====== (옵션) 단순 에코/확인용 ======
class TravelMBTI(BaseModel):
    isNewPlace: bool
    isSolo: bool
    prefersEnjoyment: bool
    isSpontaneous: bool

class PreferenceAck(BaseModel):
    ok: bool
    areaCode: int
    selected_styles: List[InputStyle]
    mbti: TravelMBTI
    notes: Optional[str]
    limit: int


class RecommendationOut(BaseModel):
    recommended: List[FestivalOut]

class RecommendationReason(BaseModel):
    score: float
    reasons: List[str]
    used_text: Optional[str] = None  # 문서화된 텍스트(가중치 반영본) 확인용

class RecommendedFestival(BaseModel):
    festival: FestivalOut
    explanation: RecommendationReason

class RecommendationOutExplained(BaseModel):
    ok: bool = True
    profile_text: str
    recommended: List[RecommendedFestival]
