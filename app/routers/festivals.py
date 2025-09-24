from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from pydantic import BaseModel

from ..db import get_session
from ..models import Festival
from ..schemas import FestivalOut

router = APIRouter(prefix="/festivals", tags=["festivals"])


# 사용자 성향 입력 스키마
class MBTIInput(BaseModel):
    isNewPlace: bool
    isSolo: bool
    prefersEnjoyment: bool
    isSpontaneous: bool

class UserPreference(BaseModel):
    styles: List[str]
    mbti: MBTIInput
    additionalInfo: Optional[str] = None
    limit: int = 5

@router.post("/random", response_model=List[FestivalOut])
async def get_random_festivals(
        preference: UserPreference,     # 요청 body
        session: AsyncSession = Depends(get_session),
):
    # 우선은 단순히 랜덤으로 추천
    stmt = select(Festival).order_by(func.rand()).limit(preference.limit)
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return rows
