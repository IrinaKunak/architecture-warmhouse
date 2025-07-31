from sqlalchemy import Column, Integer, String
from app.db import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    unit = Column(String(20))
    value = Column(String(20), nullable=True)
    status = Column(String(20), nullable=True)