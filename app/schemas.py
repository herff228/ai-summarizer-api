from pydantic import BaseModel
from datetime import datetime

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    result: str
    score: float = None  # для summarization можно не использовать, но оставим совместимость

class HistoryItem(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: datetime

class HealthResponse(BaseModel):
    status: str