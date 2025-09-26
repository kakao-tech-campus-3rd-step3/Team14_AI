from fastapi import APIRouter
from ..schemas import PreferenceIn, PreferenceAck

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/preferences", response_model=PreferenceAck, summary="설문 입력 수신(테스트)")

async def receive_preferences(payload: PreferenceIn):
    # 저장/추천 없이 입력만 검증하고 에코로 반환
    return PreferenceAck(
        ok=True,
        selected_styles=payload.festival_styles,
        mbti=payload.travel_mbti,
        notes=payload.additional_notes,
    )
