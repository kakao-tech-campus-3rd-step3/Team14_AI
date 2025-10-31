from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_session
from ..schemas import PreferenceIn, FestivalOut
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.future import select
from ..models import Festival

router = APIRouter(prefix="/ai/recommend", tags=["ai-model"])

# ✅ checkpoint 로드 (애플리케이션 시작 시 1회만)
CHECKPOINT_PATH = "/Users/haseokhyeon/Team14_AI2/checkpoint.pkl"
ckpt = joblib.load(CHECKPOINT_PATH)
fest_emb = ckpt["fest_emb"]
fest_titles = ckpt["fest_titles"]
model = ckpt.get("model", None)
num_cols = ckpt.get("num_cols", [])
cat_cols = ckpt.get("cat_cols", [])

# =======================================
# 🧠 추천 API
# =======================================
@router.post("/model", response_model=list[FestivalOut])
async def recommend_with_trained_model(
        payload: PreferenceIn,
        session: AsyncSession = Depends(get_session),
):
    """
    학습된 checkpoint.pkl 기반 추천
    - feature_json 없이 PreferenceIn으로부터 feature vector 생성
    - top_k=8개 축제 반환
    """

    # -------------------------
    # 1️⃣ DB에서 후보군 전체 불러오기
    # -------------------------
    result = await session.execute(select(Festival))
    candidates = result.scalars().all()

    if not candidates:
        return []

    # -------------------------
    # 2️⃣ 사용자 피처 벡터 구성
    # -------------------------
    # Numeric features
    nums = {c: 0.0 for c in num_cols}
    # Categorical features
    cats = {c: "__NA__" for c in cat_cols}

    # Boolean mapping
    nums.update({
        "isNewPlace": 1.0 if payload.isNewPlace else 0.0,
        "isI": 1.0 if payload.isSolo else 0.0,
        "isF": 1.0 if payload.prefersEnjoyment else 0.0,
        "isP": 1.0 if payload.isSpontaneous else 0.0,
    })

    # Style → Category 매핑
    for s in payload.styles:
        key = s.upper()
        if key in cats:
            cats[key] = "TRUE"
        elif key == "FUNEXPERIENCE":
            cats["isN"] = "TRUE"  # isN은 FUNEXPERIENCE와 매핑

    # 최종 feature dataframe (1행)
    import pandas as pd
    feat_df = pd.DataFrame([{**nums, **cats}])

    if model is not None:
        user_vec = model.predict(feat_df)[0]
    else:
        # 모델 없을 경우 임의 벡터 (debug용)
        user_vec = np.random.randn(fest_emb.shape[1])

    top_k = 8
    sims = cosine_similarity(fest_emb, user_vec.reshape(1, -1)).flatten()
    top_idx = np.argsort(-sims)[:top_k]

    recommended = []
    for i in top_idx:
        if 0 <= i < len(candidates):
            recommended.append(candidates[i])


    return recommended
