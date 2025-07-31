import random
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import Sensor

from pydantic import BaseModel
from typing import List, Optional

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


class SensorBase(BaseModel):
    name: str
    type: str
    location: str
    unit: Optional[str] = None

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    pass

class SensorOut(SensorBase):
    id: int
    value: Optional[float] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

class SensorValueUpdate(BaseModel):
    value: float
    status: str



@app.get("/api/v1/sensors", response_model=List[SensorOut])
def get_all_sensors(db: Session = Depends(get_db)):
    return db.query(Sensor).all()


@app.get("/api/v1/sensors/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@app.post("/api/v1/sensors", response_model=SensorOut)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    db_sensor = Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


@app.put("/api/v1/sensors/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: int, sensor_data: SensorUpdate, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    for field, value in sensor_data.dict().items():
        setattr(sensor, field, value)

    db.commit()
    db.refresh(sensor)
    return sensor


@app.patch("/api/v1/sensors/{sensor_id}/value", response_model=SensorOut)
def update_sensor_value(sensor_id: int, payload: SensorValueUpdate, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor.value = payload.value
    sensor.status = payload.status
    db.commit()
    db.refresh(sensor)
    return sensor


@app.delete("/api/v1/sensors/{sensor_id}", status_code=204)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    db.delete(sensor)
    db.commit()
    return

@app.get("/api/v1/temperature", response_model=SensorOut)
def get_temperature(
    location: str = Query(..., alias="location"),
    sensorID: int = Query(None, alias="sensorID"),
    db: Session = Depends(get_db)
):
    query = db.query(Sensor).filter(Sensor.location == location)
    if sensorID:
        query = query.filter(Sensor.id == sensorID)

    sensor = query.first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    simulated_value = round(random.uniform(18.0, 25.0), 2)
    sensor.value = simulated_value
    db.commit()
    db.refresh(sensor)

    return sensor


