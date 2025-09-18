from typing import Optional, Literal
from datetime import date
from sqlalchemy import (
    BigInteger, Integer, String, Date, Enum, Index
)
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

StateEnum = Enum(
    "APPROVED", "DENIED", "PROCESSING",
    name="festival_state", native_enum=False
)

class Festival(Base):
    __tablename__ = "Festival"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    areaCode:   Mapped[int]             = mapped_column(Integer, nullable=False)
    endDate:    Mapped[date]            = mapped_column(Date,    nullable=False)
    startDate:  Mapped[date]            = mapped_column(Date,    nullable=False)

    manager_id: Mapped[Optional[int]]   = mapped_column(BigInteger, nullable=True)
    homePage:   Mapped[Optional[str]]   = mapped_column(String(500),   nullable=True)
    overView:   Mapped[str]             = mapped_column(String(5000),  nullable=False)
    addr1:      Mapped[str]             = mapped_column(String(255),   nullable=False)
    addr2:      Mapped[Optional[str]]   = mapped_column(String(255),   nullable=True)
    contentId:  Mapped[Optional[str]]   = mapped_column(String(255),   nullable=True, unique=True)
    posterInfo: Mapped[str]             = mapped_column(String(255),   nullable=False)
    title:      Mapped[str]             = mapped_column(String(255),   nullable=False)
    state:      Mapped[str]             = mapped_column(StateEnum,     nullable=False)

    __table_args__ = (
        Index("idx_Festival_areaCode", "areaCode"),
        Index("idx_Festival_manager_id", "manager_id"),
    )
