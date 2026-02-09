from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime, timezone
from typing import Optional, List
import uuid
from .enums import VideoSource, Category

class Video(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: HttpUrl
    title: Optional[str] = None
    thumbnail: Optional[HttpUrl] = None
    transcript: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    category: Category = Category.OTROS
    ingredients: List[str] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    duration: Optional[int] = None  # segundos
    source: VideoSource
    saved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_note: Optional[str] = None
    embedding: Optional[List[float]] = None  # 384 dims
    language: Optional[str] = None
    telegram_user_id: Optional[int] = None
    processing_status: str = "pending"
    job_id: Optional[str] = None
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None
