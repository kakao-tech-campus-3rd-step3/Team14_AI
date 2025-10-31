# app/routers/ai_features.py
from fastapi import APIRouter
from ..schemas import PreferenceIn
from ..reco_features import split_styles_and_features

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/features/preview")
def preview_features(payload: PreferenceIn):
    canonical, feats = split_styles_and_features(payload.styles)
    feats.update({
        "isNewPlace": 1.0 if payload.isNewPlace else 0.0,
        "isI": 1.0 if payload.isSolo else 0.0,
        "isN": feats.get("isN", 0.0),
        "isF": 1.0 if payload.prefersEnjoyment else 0.0,
        "isP": 1.0 if payload.isSpontaneous else 0.0,
    })
    return {
        "ok": True,
        "canonical_styles": canonical,
        "features": feats,
        "saved": False,
    }
