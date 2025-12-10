from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class ReservationData(BaseModel):
    date: datetime
    email: str
    name: str
    numberOfPeople: int = Field(..., gt=0, alias="numberOfPeople")
    phone: str
    reason: str
    reservationType: Literal["time", "event"] = Field(..., alias="reservationType")
    timestamp: datetime
    
    class Config:
        populate_by_name = True
    
    def to_sheet_values(self) -> list:
        """Convierte el modelo a una lista de valores para Google Sheets"""
        return [
            self.name,
            self.email,
            self.phone,
            self.numberOfPeople,
            self.reservationType,
            self.timestamp.isoformat(),
            self.date.isoformat(),
            self.reason
        ]