from pydantic import BaseModel
from typing import List, Optional

class TrendItem(BaseModel):
    rank: str
    text: str
    link: str
    duration: str

class TrendResponse(BaseModel):
    country: str
    trends: List[TrendItem]
