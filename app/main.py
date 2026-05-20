from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import engine, get_db, Base
from app.routes import analyze, history
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Summarizer API")

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Подключение роутов
app.include_router(analyze.router, tags=["Analysis"])
app.include_router(history.router, tags=["History"])

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        logger.info("Health check OK")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Database unavailable")