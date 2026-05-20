from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.db import get_db

router = APIRouter()

@router.get("/history", response_model=list[schemas.HistoryItem])
def get_history(db: Session = Depends(get_db)):
    records = db.query(models.RequestHistory).order_by(models.RequestHistory.created_at.desc()).limit(20).all()
    return records

@router.get("/history/{record_id}", response_model=schemas.HistoryItem)
def get_history_item(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.RequestHistory).filter(models.RequestHistory.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record