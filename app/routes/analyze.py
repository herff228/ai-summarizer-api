from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, ml_service
from app.db import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=schemas.AnalyzeResponse)
def analyze(request: schemas.AnalyzeRequest, db: Session = Depends(get_db)):
    # Валидация
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 chars)")
    
    try:
        # Суммаризация
        summary = ml_service.summarize_text(request.text)
        
        # Сохранение в БД
        history = models.RequestHistory(
            input_text=request.text,
            result_text=summary,
            model_name=ml_service._model_name
        )
        db.add(history)
        db.commit()
        
        logger.info(f"Request processed, id={history.id}")
        
        return schemas.AnalyzeResponse(result=summary)
    
    except Exception as e:
        logger.error(f"Model error: {e}")
        raise HTTPException(status_code=500, detail="Summarization failed")