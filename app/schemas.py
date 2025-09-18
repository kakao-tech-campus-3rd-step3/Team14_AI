from typing import Optional, Literal
from pydantic import BaseModel
from datetime import date

class FestivalOut(BaseModel):
    id: int
    areaCode: int
    endDate: date
    startDate: date
    manager_id: Optional[int]
    homePage: Optional[str]
    overView: str
    addr1: str
    addr2: Optional[str]
    contentId: Optional[str]
    posterInfo: str
    title: str
    state: Literal["APPROVED", "DENIED", "PROCESSING"]

    class Config:
        from_attributes = True
