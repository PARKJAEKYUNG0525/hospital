from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import List

from .appointments import Appointment

class Prescription(Base):
    __tablename__ = "prescriptions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id", ondelete="CASCADE"), index=True, nullable=False)
    medicine_name: Mapped[str] = mapped_column(String(255), nullable=False)
    #created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    appointment: Mapped["Appointment"] = relationship(
        "Appointment",
        back_populates="prescriptions"
    )