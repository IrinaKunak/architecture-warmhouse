from pydantic import BaseModel
from typing import Optional


class SensorCreate(BaseModel):
    name: str
    type: str
    location: str
    unit: Optional[str] = None


class SensorOut(SensorCreate):
    id: int
    value: float
    status: str

    class Config:
        orm_mode = True
