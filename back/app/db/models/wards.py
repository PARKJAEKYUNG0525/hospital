from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import List

from .doctors import Doctor

class Ward(Base):
    __tablename__ = "wards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ward_name: Mapped[str] = mapped_column(String(50))
    room_no: Mapped[int] = mapped_column()
    bed_count: Mapped[int] = mapped_column(default=1)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))

    doctor: Mapped["Doctor"] = relationship(
        "Doctor", back_populates="wards"
    )