# app/routers/festivals.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from ..db import get_session
from ..models import Festival
from ..schemas import FestivalOut

router = APIRouter(prefix="/festivals", tags=["festivals"])

# styles 허용 값(9개)
FestivalStyle = Literal[
    "TRADITIONAL", "ART_PERFORMANCE", "FOOD",
    "NATURE", "EXPERIENCE", "TRENDY",
    "COMMUNITY", "LOCAL", "INTERNATIONAL"
]

class UserPreferenceV2(BaseModel):
    areaCode: int
    styles: List[FestivalStyle] = Field(..., min_items=1, description="축제 스타일 최소 1개 이상")
    isNewPlace: bool
    isSolo: bool
    prefersEnjoyment: bool
    isSpontaneous: bool
    additionalInfo: Optional[str] = None
    limit: int = Field(5, ge=1, le=50)

@router.post("/random", response_model=List[FestivalOut])
async def get_random_festivals(
        preference: UserPreferenceV2,
        session: AsyncSession = Depends(get_session),
):
    # 현재는 성향을 사용하지 않고 랜덤 추출만 수행
    stmt = select(Festival).order_by(func.rand()).limit(preference.limit)
    result = await session.execute(stmt)
    return result.scalars().all()
