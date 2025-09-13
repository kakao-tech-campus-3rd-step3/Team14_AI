from typing import Optional
from datetime import date  # ✅ Python 타입
from sqlalchemy import BigInteger, Integer, String, Date, Text  # ✅ Date는 DB 컬럼 타입으로만 사용
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Festival(Base):
    __tablename__ = "festival"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    addr1: Mapped[Optional[str]] = mapped_column(String(255))
    addr2: Mapped[Optional[str]] = mapped_column(String(255))
    areaCode: Mapped[Optional[int]] = mapped_column(Integer)
    contentId: Mapped[Optional[str]] = mapped_column(String(255))
    endDate: Mapped[Optional[date]] = mapped_column(Date)       # ✅ Python date
    homePage: Mapped[Optional[str]] = mapped_column(String(500))
    imageUrl: Mapped[Optional[str]] = mapped_column(String(255))
    overView: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    startDate: Mapped[Optional[date]] = mapped_column(Date)     # ✅ Python date
