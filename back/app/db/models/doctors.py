from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import List

from .appointments import Appointment

class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    specialty: Mapped[str] = mapped_column(String(100))
    license_no: Mapped[str] = mapped_column(String(50), unique=True)

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="doctor",
        cascade="all,delete"
    )
    wards = relationship(
        "Ward", back_populates="doctor"
    )