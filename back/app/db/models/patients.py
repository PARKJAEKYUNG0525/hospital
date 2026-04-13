from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String,Date
from typing import List

from .appointments import Appointment

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10),nullable=False)

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",back_populates="patient", cascade="all, delete-orphan"
    )