import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from loguru import logger

class AutoHedgeOutput(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    thesis: Optional[str] = None
    risk_assessment: Optional[str] = None
    order: Optional[str] = None
    decision: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    current_stock: str

class AutoHedgeOutputMain(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    stocks: Optional[list] = None
    task: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    logs: List[AutoHedgeOutput] = []

def setup_logging():
    logger.add("logs/autohedge.log", rotation="500 MB", level="INFO")
