from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from .patients import Patient
    from .doctors import Doctor
    from .prescriptions import Prescription

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False) # NULL 허용 여부 명시
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="SCHEDULED")
    
    appointment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)


    patient: Mapped["Patient"] = relationship("Patient", back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="appointments")
    prescriptions: Mapped[List["Prescription"]] = relationship(
        "Prescription",
        back_populates="appointment",
        cascade="all, delete-orphan" 
    )

    