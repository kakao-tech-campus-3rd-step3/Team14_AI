# app/schemas.py
from typing import Optional, List, Literal
from datetime import date
from pydantic import BaseModel, Field


# ==============================
# 축제 정보 응답 DTO
# ==============================
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


# ==============================
# 설문 입력 관련 스키마
# ==============================

# 1) 축제 스타일(9개 고정)
FestivalStyle = Literal[
    "TRADITIONAL", "ART_PERFORMANCE", "FOOD",
    "NATURE", "EXPERIENCE", "TRENDY",
    "COMMUNITY", "LOCAL", "INTERNATIONAL"
]

# 2) MBTI: 지금 스펙은 평탄화된 boolean 필드 (isNewPlace, isSolo, ...)
#    - 라우터에서 그대로 쓰려면 이 모델을 응답/에코 용도로 사용
class TravelMBTI(BaseModel):
    isNewPlace: bool
    isSolo: bool
    prefersEnjoyment: bool
    isSpontaneous: bool


# 3) 전체 입력 페이로드 (현재 프론트에서 보내는 JSON과 1:1 매칭)
class PreferenceIn(BaseModel):
    areaCode: int
    styles: List[FestivalStyle] = Field(..., min_items=1, description="축제 스타일 최소 1개 이상")
    # 평탄화된 MBTI 필드 (중첩 아님)
    isNewPlace: bool
    isSolo: bool
    prefersEnjoyment: bool
    isSpontaneous: bool
    additionalInfo: Optional[str] = Field(None, max_length=500, description="자유기입(최대 500자)")
    limit: int = Field(5, ge=1, le=50)


# 4) 응답(테스트용 에코)
class PreferenceAck(BaseModel):
    ok: bool
    areaCode: int
    selected_styles: List[FestivalStyle]
    mbti: TravelMBTI
    notes: Optional[str]
    limit: int
    # app/schemas.py (추가/정리)

# ---- 이유가 없는 간단 추천 응답 ----
class RecommendationOut(BaseModel):
    profile_text: str
    recommended: List[FestivalOut]

# ---- 이유(설명) 포함 추천 응답 ----
class RecommendationReason(BaseModel):
    score: float                # (raw cosine 또는 보정 전/후 점수)
    reasons: List[str]          # 사람이 읽을 설명 포인트 목록
    used_text: str

class RecommendedFestival(BaseModel):
    festival: FestivalOut
    explanation: RecommendationReason

class RecommendationOutExplained(BaseModel):
    profile_text: str
    recommended: List[RecommendedFestival]
