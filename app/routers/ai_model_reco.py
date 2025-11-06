from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple, Optional
import re, numpy as np, pandas as pd, joblib
from difflib import SequenceMatcher
from sklearn.metrics.pairwise import cosine_similarity

from ..db import get_session
from ..schemas import FestivalOut, PreferenceIn
from ..models import Festival

import numpy as np


router = APIRouter(prefix="/ai/recommend", tags=["ai-model"])

# ====== 체크포인트 로드 ======
CHECKPOINT_PATH = "app/models/checkpoint.pkl"
ckpt = joblib.load(CHECKPOINT_PATH)
tfidf = ckpt["tfidf"]
svd = ckpt["svd"]
fest_emb = ckpt["fest_emb"]
fest_titles = ckpt["fest_titles"]
fest_keys = ckpt.get("fest_keys", None)
model = ckpt.get("model", None)
num_cols = ckpt.get("num_cols", []) or []
cat_cols = ckpt.get("cat_cols", []) or []

# ---------- 테마 사전 / 부정 패턴 ----------
SEA_SYNS = ["바다","해변","바닷가","해안","연안","해수욕장","해변가","해양","섬","바다뷰","바닷물","항구","해돋이","일출","바다낚시","스노클링","조개잡이","바다축제","바다공원"]
MOUNTAIN_SYNS = ["산","등산","계곡","산책로","트레킹","폭포","암벽","산림","숲","야영","캠핑","림파크","치유의숲"]
CITY_SYNS = ["도심","도시","야경","야시장","거리공연","카페","미술관","박물관","쇼핑","페스티벌","도시축제","거리축제"]
RIVER_LAKE_SYNS = ["강","천","하천","호수","저수지","강변","수변","수상","강축제","호수공원","수변공원"]
FOOD_SYNS = ["음식","먹거리","맛집","길거리음식","푸드트럭","시식","푸드","미식","로컬푸드","전통음식","한식","디저트","베이커리","먹거리축제"]
MUSIC_SYNS = ["음악","버스킹","공연","라이브","콘서트","락","재즈","힙합","클래식","DJ","댄스","뮤직페스티벌"]
HISTORY_SYNS = ["역사","유적","문화재","전통","국악","민속","퍼레이드","제례","풍물","전통공연","궁중","의장대","시가행진"]
FAMILY_SYNS = ["가족","아이","키즈","유아","체험","놀이","체험부스","교육","안전","피크닉","패밀리","유모차"]
NIGHT_SYNS = ["야간","밤","야경","빛축제","불빛","조명","라이트쇼","레이저쇼","불꽃놀이","나이트","야간개장"]
PHOTO_SYNS = ["사진","포토","포토존","인생샷","출사","촬영","스냅","전시","포토스팟","사진전"]
ROMANCE_SYNS = ["데이트","연인","분위기","로맨틱","산책","야경데이트","감성","감성스팟"]
MARKET_SYNS = ["마켓","플리마켓","프리마켓","벼룩시장","수공예","핸드메이드","판매부스","로컬장터","농특산물"]
FLOWER_SYNS = ["꽃","꽃축제","튤립","벚꽃","코스모스","유채꽃","핑크뮬리","장미","수국","꽃길","플라워가든"]
DRINK_SYNS = ["맥주","수제맥주","와인","막걸리","전통주","칵테일","바텐딩","시음","주류","술","비어"]

THEME_LEX: Dict[str, List[str]] = {
    "SEA": SEA_SYNS, "MOUNTAIN": MOUNTAIN_SYNS, "CITY": CITY_SYNS, "RIVER_LAKE": RIVER_LAKE_SYNS,
    "FOOD": FOOD_SYNS, "MUSIC": MUSIC_SYNS, "HISTORY": HISTORY_SYNS, "FAMILY": FAMILY_SYNS,
    "NIGHT": NIGHT_SYNS, "PHOTO": PHOTO_SYNS, "ROMANCE": ROMANCE_SYNS, "MARKET": MARKET_SYNS,
    "FLOWER": FLOWER_SYNS, "DRINK": DRINK_SYNS,
}

NEG_PATTERNS = [
    r"싫어", r"싫다", r"별로", r"안\s*좋아", r"안좋아", r"절대", r"전혀", r"도무지", r"도저히",
    r"안\s*가", r"가(기|는|는\s*걸)?\s*싫", r"가고\s*싶지\s*않", r"가지\s*않", r"가진\s*않", r"가기\s*싫",
    r"비선호", r"미선호", r"not\s+go", r"never\s+go", r"don['’]t\s+want\s+to\s+go",
]
NEG_COMPILED = [re.compile(p, flags=re.IGNORECASE) for p in NEG_PATTERNS]

POS_PATTERNS = [
    r"좋아", r"좋다", r"좋아해", r"선호", r"원해", r"가고\s*싶", r"관심\s*있",
    r"좋음", r"취향", r"끌려", r"가자", r"보고\s*싶", r"즐기고\s*싶",
]
POS_COMPILED = [re.compile(p, flags=re.IGNORECASE) for p in POS_PATTERNS]

# ---------- 유틸 ----------
KST = timezone(timedelta(hours=9))

def norm_key(s) -> str:
    if s is None: return ""
    s = str(s).strip().lower()
    s = re.sub(r"(축제|페스티벌|엑스포|박람회)$", "", s)
    s = re.sub(r"[^0-9a-zA-Z가-힣 ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s

def cosine_batch(A: np.ndarray, v: np.ndarray) -> np.ndarray:
    An = np.linalg.norm(A, axis=1) + 1e-12
    vn = np.linalg.norm(v) + 1e-12
    return (A @ v) / (An * vn)

def window_has_negation(text: str, span: Tuple[int, int], window: int = 14) -> bool:
    s, e = span
    left = max(0, s - window)
    right = min(len(text), e + window)
    seg = (text or "").lower()[left:right]
    return any(p.search(seg) for p in NEG_COMPILED)

def embed_terms(terms: List[str]) -> np.ndarray:
    if not terms: return np.zeros(svd.n_components)
    X = tfidf.transform([" ".join(terms)])
    return svd.transform(X)[0]

def fuzzy_find_index(title: str, threshold: float = 0.75) -> Optional[int]:
    t = norm_key(title)
    keys = fest_keys if fest_keys is not None else fest_titles
    best_i, best_r = None, 0.0
    for i, ref in enumerate(keys):
        r = SequenceMatcher(None, t, norm_key(ref)).ratio()
        if r > best_r:
            best_i, best_r = i, r
    return best_i if best_r >= threshold else None

def embed_festival_text(title: str, overview: str) -> np.ndarray:
    txt = f"{title or ''} {overview or ''}".strip()
    if not txt:
        return np.zeros(svd.n_components)
    X = tfidf.transform([txt])
    return svd.transform(X)[0]

def build_feature_df_from_payload(payload: PreferenceIn) -> pd.DataFrame:
    nums = {c: 0.0 for c in (num_cols or [])}
    cats = {c: "__NA__" for c in (cat_cols or [])}

    bool_map = {
        "isNewPlace": payload.isNewPlace,
        "isI": payload.isSolo,
        "isF": payload.prefersEnjoyment,
        "isP": payload.isSpontaneous,
    }
    for k, v in bool_map.items():
        if k in nums:
            nums[k] = 1.0 if v else 0.0

    for s in (payload.styles or []):
        key = str(s).upper()
        if key in cats:
            cats[key] = "TRUE"
        if key == "FUNEXPERIENCE" and "isN" in cats:
            cats["isN"] = "TRUE"

    return pd.DataFrame([{**nums, **cats}])

def window_has(text: str, span: Tuple[int,int], regexes: List[re.Pattern], window: int = 14) -> bool:
    s, e = span
    left = max(0, s - window)
    right = min(len(text), e + window)
    seg = (text or "").lower()[left:right]
    return any(r.search(seg) for r in regexes)


def expand_query_with_window_negation(query: str) -> Tuple[List[str], List[str]]:
    q = re.sub(r"\s+", " ", str(query or "")).strip().lower()
    if not q:
        return [], []

    vocab = sorted({w for vs in THEME_LEX.values() for w in vs}, key=len, reverse=True)
    hits: List[Tuple[str, Tuple[int,int]]] = []
    for term in vocab:
        for m in re.finditer(re.escape(term), q):
            hits.append((term, (m.start(), m.end())))
    if not hits:
        for coarse in ["바다","해변","산","계곡","도심","강","호수","음식","공연","사진","마켓","꽃","맥주","와인","밤","데이트"]:
            for m in re.finditer(coarse, q):
                hits.append((coarse, (m.start(), m.end())))

    def related(tok: str) -> List[str]:
        for k, vs in THEME_LEX.items():
            if tok in vs:
                return vs
        mapping = {"바다":"SEA","해변":"SEA","산":"MOUNTAIN","계곡":"MOUNTAIN","도심":"CITY",
                   "강":"RIVER_LAKE","호수":"RIVER_LAKE","음식":"FOOD","공연":"MUSIC",
                   "사진":"PHOTO","마켓":"MARKET","꽃":"FLOWER","맥주":"DRINK","와인":"DRINK",
                   "밤":"NIGHT","데이트":"ROMANCE"}
        return THEME_LEX.get(mapping.get(tok, ""), [])

    pos_terms, neg_terms = [], []

    global_neg = any(r.search(q) for r in NEG_COMPILED)
    global_pos = any(r.search(q) for r in POS_COMPILED)

    for tok, span in hits:
        rel = related(tok)
        if not rel:
            continue

        local_neg = window_has(q, span, NEG_COMPILED, window=14)
        local_pos = window_has(q, span, POS_COMPILED, window=14)

        # 우선순위: (1) 로컬 신호 > (2) 전역 신호 > (3) 중립(긍정 처리)
        if local_neg and not local_pos:
            for t in rel:
                if t not in neg_terms:
                    neg_terms.append(t)
        elif local_pos and not local_neg:
            for t in rel:
                if t not in pos_terms:
                    pos_terms.append(t)
        else:
            # 로컬이 둘 다 있거나 둘 다 없으면 전역에 따라 분기
            if global_neg and not global_pos:
                for t in rel:
                    if t not in neg_terms:
                        neg_terms.append(t)
            elif global_pos and not global_neg:
                for t in rel:
                    if t not in pos_terms:
                        pos_terms.append(t)
            else:
                # 전역도 애매하면 기본은 '긍정'으로 분류(언급=관심 가정)
                for t in rel:
                    if t not in pos_terms:
                        pos_terms.append(t)

    # 상충 정리: neg에 있으면 pos에서 제거
    pos_terms = sorted(set(pos_terms) - set(neg_terms))
    neg_terms = sorted(set(neg_terms))
    return pos_terms, neg_terms


@router.post("/model", response_model=list[FestivalOut])
async def recommend(payload: PreferenceIn, session: AsyncSession = Depends(get_session)):
    today = datetime.now(KST).date()

    if int(getattr(payload, "areaCode", 0) or 0) == 0:
        q = select(Festival).where(Festival.endDate > today)
    else:
        q = select(Festival).where(
            and_(
                Festival.areaCode == payload.areaCode,
                Festival.endDate > today
            )
        )

    candidates = (await session.execute(q)).scalars().all()
    if not candidates:
        return []


    # 1) 후보 임베딩
    fest_vecs = []
    for f in candidates:
        idx = fuzzy_find_index(f.title)
        vec = fest_emb[idx] if idx is not None else embed_festival_text(f.title, f.overView or "")
        fest_vecs.append(vec)
    fest_vecs = np.stack(fest_vecs, axis=0)  # [N, D]

    # 2) 사용자 임베딩
    feat_df = build_feature_df_from_payload(payload)
    user_vec = model.predict(feat_df)[0] if model is not None else np.random.randn(fest_emb.shape[1])

    # 3) 추가 텍스트 선호/비선호
    pos_terms, neg_terms = expand_query_with_window_negation(payload.additionalInfo or "")
    pos_vec = embed_terms(pos_terms)
    neg_vec = embed_terms(neg_terms)

    # 4) 점수 계산 (설문/텍스트)
    w_model, w_pos, w_neg = 0.7, 0.4, 0.6
    model_sim = cosine_batch(fest_vecs, user_vec)
    pos_sim   = cosine_batch(fest_vecs, pos_vec) if np.any(pos_vec) else np.zeros(len(candidates))
    neg_sim   = cosine_batch(fest_vecs, neg_vec) if np.any(neg_vec) else np.zeros(len(candidates))
    base_scores = w_model * model_sim + w_pos * pos_sim - w_neg * neg_sim

    # 5) 랜덤 가중치 추가 (다양성 확보)
    np.random.seed()  # 요청마다 다른 랜덤
    RAND_MAX = 0.15   # 다양성 강도 (0.1~0.4 사이 추천)
    random_scores = np.random.uniform(low=0, high=RAND_MAX, size=len(base_scores))
    final_scores = base_scores + random_scores

    # 6) 최종 상위 2개 추천
    top_indices = np.argsort(-final_scores)[:2]
    picked = [candidates[i] for i in top_indices]

    return [FestivalOut.model_validate(f, from_attributes=True) for f in picked]
