# app/routers/festivals.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from ..schemas import (
    PreferenceIn,
    RecommendationOut,
    RecommendationOutExplained,
    RecommendedFestival,
    RecommendationReason,
    FestivalOut,
)
from ..db import get_session
from ..models import Festival
from ..reco import build_user_profile_text, rank_simple, rank_with_explanations, Doc


router = APIRouter(prefix="/festivals", tags=["festivals"])

FestivalStyle = Literal[
    "TRADITIONAL", "ART_PERFORMANCE", "FOOD",
    "NATURE", "EXPERIENCE", "TRENDY",
    "COMMUNITY", "LOCAL", "INTERNATIONAL"
]

class UserPreferenceV2(BaseModel):
    areaCode: int
    styles: List[FestivalStyle] = Field(..., min_items=1)
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
    stmt = select(Festival).order_by(func.rand()).limit(preference.limit)
    result = await session.execute(stmt)
    return result.scalars().all()

def _build_docs(candidates: List[Festival]) -> List[Doc]:
    docs: List[Doc] = []
    for f in candidates:
        # 중요 필드에 가중치 주고 싶으면 반복해서 붙이기
        parts = []
        if f.title:    parts.append((f.title + " ") * 3)
        if f.overView: parts.append((f.overView + " ") * 2)
        # if f.addr1:    parts.append(f.addr1)
        # if f.addr2:    parts.append(f.addr2 or "")
        # if f.homePage: parts.append(f.homePage)
        text = "\n".join([p for p in parts if p and p.strip()])
        docs.append(Doc(key=str(f.id), text=text))

    return docs

def _fetch_candidates(session: AsyncSession, area_code: int, limit: int) -> List[Festival]:
    raise NotImplementedError

@router.post(
    "/recommend",
    response_model=List[FestivalOut],
    summary="성향 기반 추천 (이유 없음)"
)

async def recommend_simple(payload: PreferenceIn, session: AsyncSession = Depends(get_session)):
    # 1) 사용자 프로필 텍스트
    profile_text = build_user_profile_text(
        area_code=payload.areaCode,
        styles=payload.styles,
        is_new_place=payload.isNewPlace,
        is_solo=payload.isSolo,
        prefers_enjoyment=payload.prefersEnjoyment,
        is_spontaneous=payload.isSpontaneous,
        additional=payload.additionalInfo,
    )

    # 2) 후보군 조회 (areaCode 우선, 부족 시 보충)
    q = select(Festival).where(Festival.areaCode == payload.areaCode).limit(max(2000, payload.limit * 4))
    r = await session.execute(q)
    candidates = list(r.scalars().all())

    if len(candidates) < payload.limit:
        q2 = (
            select(Festival)
            .where(Festival.areaCode != payload.areaCode)
            .order_by(func.rand())
            .limit(payload.limit * 4)
        )
        r2 = await session.execute(q2)
        candidates.extend(list(r2.scalars().all()))

    if not candidates:
        return []

    # 3) 문서화 & 랭킹
    docs = _build_docs(candidates)
    top_ids = rank_simple(profile_text, docs, top_k=payload.limit)
    id_map = {f.id: f for f in candidates}
    ranked: List[FestivalOut] = [id_map[int(fid)] for fid in top_ids if int(fid) in id_map]

    return ranked

@router.post("/recommend/explain", response_model=RecommendationOutExplained, summary="성향 기반 추천 (설명 포함)")
async def recommend_with_reasons(payload: PreferenceIn, session: AsyncSession = Depends(get_session)):
    profile_text = build_user_profile_text(
        area_code=payload.areaCode,
        styles=payload.styles,
        is_new_place=payload.isNewPlace,
        is_solo=payload.isSolo,
        prefers_enjoyment=payload.prefersEnjoyment,
        is_spontaneous=payload.isSpontaneous,
        additional=payload.additionalInfo,
    )

    q = select(Festival).where(Festival.areaCode == payload.areaCode).limit(max(2000, payload.limit * 4))
    r = await session.execute(q)
    candidates = list(r.scalars().all())
    if len(candidates) < payload.limit:
        q2 = (
            select(Festival)
            .where(Festival.areaCode != payload.areaCode)
            .order_by(func.rand())
            .limit(payload.limit * 4)
        )
        r2 = await session.execute(q2)
        candidates.extend(list(r2.scalars().all()))

    if not candidates:
        return RecommendationOutExplained(ok=True, profile_text=profile_text, recommended=[])

    # 3) 문서화
    docs = _build_docs(candidates)
    doc_map = {doc.key: doc.text for doc in docs}

    # 4) 유사도 + 설명
    ranked = rank_with_explanations(profile_text, docs, top_k=payload.limit)

    id_map = {f.id: f for f in candidates}
    out: List[RecommendedFestival] = []
    for key, raw_score, reasons in ranked:
        fid = int(key)
        if fid in id_map:
            out.append(
                RecommendedFestival(
                    festival=id_map[fid],
                    explanation=RecommendationReason(
                        score=raw_score,
                        reasons=reasons,
                        used_text=doc_map.get(key, "")
                    )
                )
            )

    return RecommendationOutExplained(ok=True, profile_text=profile_text, recommended=out)

@router.get("/all", response_model=List[FestivalOut], summary="모든 축제 목록 (과거/미래 포함, 이름 검색 가능)")
async def get_all_festivals(
        session: AsyncSession = Depends(get_session),
        title: Optional[str] = Query(None, description="축제 이름 일부로 검색"),
        limit: int = Query(1000, ge=1, le=5000, description="반환할 최대 축제 개수"),
        offset: int = Query(0, ge=0, description="페이지 오프셋"),
):
    # 기본 쿼리: 모든 축제 포함
    stmt = select(Festival)

    # 이름 필터 (부분 일치)
    if title:
        stmt = stmt.where(Festival.title.like(f"%{title}%"))

    # 정렬 및 페이지네이션
    stmt = stmt.order_by(Festival.startDate.asc()).limit(limit).offset(offset)

    # 실행
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return rows
