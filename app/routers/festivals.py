from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from ..db import get_session
from ..models import Festival
from ..schemas import FestivalOut

router = APIRouter(prefix="/festivals", tags=["festivals"])

@router.get("/random", response_model=List[FestivalOut])
async def get_random_festivals(
    limit: int = Query(5, ge=1, le=50, description="반환할 축제 개수 (기본 5, 최대 50)"),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Festival).order_by(func.rand()).limit(limit)
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return rows
