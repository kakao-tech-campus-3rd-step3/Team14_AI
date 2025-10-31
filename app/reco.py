# app/reco.py
from typing import List, Dict, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from difflib import SequenceMatcher

STYLE_KEYWORDS: Dict[str, List[str]] = {
    "TRADITIONAL":    ["전통", "문화", "국악", "민속", "역사"],
    "ART_PERFORMANCE":["공연", "콘서트", "연극", "무용", "뮤직", "페스티벌"],
    "FOOD":           ["먹거리", "푸드", "야시장", "미식", "향토음식", "푸드트럭"],
    "NATURE":         ["자연", "바다", "산", "경관", "캠핑", "휴식", "숲", "해변"],
    "EXPERIENCE":     ["체험", "참여", "워크숍", "플리마켓", "핸즈온", "퍼레이드"],
    "TRENDY":         ["트렌디", "핫플", "인스타", "MZ", "도시축제", "힙"],
    "COMMUNITY":      ["지역주민", "커뮤니티", "소통", "마을", "로컬행사"],
    "LOCAL":          ["지역특색", "향토", "전통시장", "로컬브랜드"],
    "INTERNATIONAL":  ["국제", "글로벌", "외국인", "다문화"]
}

def build_user_profile_text(
        area_code: int,
        styles: List[str],
        is_new_place: bool,
        is_solo: bool,
        prefers_enjoyment: bool,
        is_spontaneous: bool,
        additional: str | None = None,
) -> str:
    # area_code는 SQL 필터로만 사용하고, 텍스트에서는 제외
    lines = []

    chosen_kw: List[str] = []
    for s in styles:
        chosen_kw.extend(STYLE_KEYWORDS.get(s, [s]))

    if styles:
        lines.append("관심 스타일: " + " ".join(styles))
    if chosen_kw:
        # (가중치 주고 싶으면 키워드를 중복 기재하면 됨)
        lines.append("스타일 키워드: " + " ".join(chosen_kw))

    lines.append("여행 성향: " + " ".join([
        "새로운곳" if is_new_place else "익숙한곳",
        "혼자" if is_solo else "동행선호",
        "즐거움중시" if prefers_enjoyment else "유익함중시",
        "즉흥적" if is_spontaneous else "계획적"
    ]))

    if additional:
        lines.append("추가 메모: " + additional)

    return "\n".join(lines)


@dataclass
class Doc:
    key: str
    text: str
    styles_hit: List[str] | None = None  # 스타일 키워드 매칭 결과(설명용)

_KO_STOP_SUFFIXES = ("축제", "행사")
_KO_STOP_TOKENS = {"축제", "행사", "공연", "페스티벌", "축제는", "행사는"}  # 원하면 확장

# ---- A) 간단 랭킹 (이유 없음) ----
def rank_simple(user_text: str, docs: List[Doc], top_k: int = 8) -> List[str]:
    if not docs:
        return []
    corpus = [user_text] + [d.text for d in docs]
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(4, 6), sublinear_tf=True, dtype=np.float32)
    X = vec.fit_transform(corpus)
    sims = cosine_similarity(X[0:1], X[1:]).flatten()
    order = sims.argsort()[::-1][:top_k]
    return [docs[i].key for i in order]

def _normalize_phrase(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w가-힣 ]+", "", s)
    for suf in _KO_STOP_SUFFIXES:
        if s.endswith(suf) and len(s) > len(suf) + 1:
            s = s[: -len(suf)]
    return s.strip()

def _too_similar(a: str, b: str, th: float = 0.85) -> bool:
    if not a or not b: return False
    return SequenceMatcher(None, a, b).ratio() >= th

def _dedupe_phrases(cands: list[str], max_k: int = 6) -> list[str]:
    normed = []
    for x in cands:
        n = _normalize_phrase(x)
        if len(n) < 2: continue
        if n in _KO_STOP_TOKENS: continue
        normed.append(n)
    normed.sort(key=lambda s: len(s), reverse=True)
    kept: list[str] = []
    for cand in normed:
        if any(cand in k for k in kept):  # 부분문자열 억제
            continue
        if any(_too_similar(cand, k) for k in kept):
            continue
        kept.append(cand)
        if len(kept) >= max_k:
            break
    return kept

def _extract_explained_overlap(vec: TfidfVectorizer, user_vec, doc_vec, top_n=12, show_k=4) -> list[str]:
    prod = user_vec.multiply(doc_vec)
    if prod.nnz == 0: return []
    coo = prod.tocoo()
    feats = vec.get_feature_names_out()
    idx_sorted = np.argsort(coo.data)[::-1][:top_n]
    raw = []
    for i in idx_sorted:
        ngram = feats[coo.col[i]].strip()
        if len(ngram) >= 3:
            raw.append(ngram)
    return _dedupe_phrases(raw, max_k=show_k)

def rank_with_explanations(
        user_text: str, docs: List[Doc], top_k: int = 5
) -> List[tuple[str, float, list[str]]]:
    """
    반환: [(doc_key, raw_cosine_score, reasons[]), ...]
    """
    if not docs:
        return []
    corpus = [user_text] + [d.text for d in docs]
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(4, 6), sublinear_tf=True, dtype=np.float32)
    X = vec.fit_transform(corpus)
    user_v, doc_m = X[0:1], X[1:]
    sims = cosine_similarity(user_v, doc_m).flatten()
    order = sims.argsort()[::-1][:top_k]

    out = []
    for idx in order:
        reasons = _extract_explained_overlap(vec, user_v, doc_m[idx:idx+1], top_n=12, show_k=4)
        out.append((docs[idx].key, float(sims[idx]), reasons))

    return out
