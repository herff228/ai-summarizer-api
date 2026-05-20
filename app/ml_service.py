from transformers import pipeline
import os
import logging

logger = logging.getLogger(__name__)

_model = None
_model_name = os.getenv("HF_MODEL_NAME", "facebook/bart-large-cnn")
_max_length = int(os.getenv("MAX_LENGTH", 150))
_min_length = int(os.getenv("MIN_LENGTH", 30))

def load_model():
    global _model
    if _model is None:
        try:
            logger.info(f"Loading summarization model: {_model_name}")
            _model = pipeline("summarization", model=_model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    return _model

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) < 10:
        raise ValueError("Text too short for summarization")
    
    model = load_model()
    result = model(text, max_length=_max_length, min_length=_min_length, do_sample=False)
    return result[0]['summary_text']