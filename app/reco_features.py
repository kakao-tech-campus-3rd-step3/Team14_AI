# app/reco_features.py  (새 파일 혹은 기존 reco.py에 추가)
from typing import List, Dict, Tuple

CANONICAL = {
    "TRADITIONAL","ART_PERFORMANCE","FOOD",
    "NATURE","EXPERIENCE","TRENDY",
    "COMMUNITY","LOCAL","INTERNATIONAL"
}

def split_styles_and_features(styles: List[str]) -> Tuple[List[str], Dict[str, float]]:
    s = set(styles)
    canonical = [st for st in styles if st in CANONICAL]

    nature = 1.0 if "NATURE" in s else (0.0 if "CITY" in s else 0.0)
    resting = 1.0 if "RESTING" in s else (0.0 if "ACTIVITY" in s else 0.0)
    photoshot = 1.0 if "PHOTOSHOT" in s else 0.0
    knownplace = 1.0 if "KNOWNPLACE" in s else 0.0
    funexperience = 1.0 if "FUNEXPERIENCE" in s else 0.0

    features = {
        "nature": nature,
        "resting": resting,
        "photoshot": photoshot,
        "knownplace": knownplace,
        "isN": funexperience,
    }
    return canonical, features

