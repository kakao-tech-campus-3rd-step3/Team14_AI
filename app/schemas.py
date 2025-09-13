from typing import Optional
from pydantic import BaseModel
from datetime import date

class FestivalOut(BaseModel):
    id: int
    contentId: Optional[str]
    title: Optional[str]
    areaCode: Optional[int]
    addr1: Optional[str]
    addr2: Optional[str]
    startDate: Optional[date]
    endDate: Optional[date]
    homePage: Optional[str]
    imageUrl: Optional[str]
    overView: Optional[str]

    class Config:
        from_attributes = True
