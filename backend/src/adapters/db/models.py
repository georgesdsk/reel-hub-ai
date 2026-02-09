from sqlalchemy import Column, String, Integer, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid
from datetime import datetime, timezone
from src.domain.entities.enums import VideoSource, Category

class Base(DeclarativeBase):
    pass

class VideoModel(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)
    thumbnail: Mapped[str] = mapped_column(String, nullable=True)
    transcript: Mapped[str] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(PG_ARRAY(String), default=[])
    category: Mapped[Category] = mapped_column(Enum(Category), default=Category.OTROS)
    ingredients: Mapped[list[str]] = mapped_column(PG_ARRAY(String), default=[])
    steps: Mapped[list[str]] = mapped_column(PG_ARRAY(String), default=[])
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    source: Mapped[VideoSource] = mapped_column(Enum(VideoSource), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_note: Mapped[str] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=True)
    language: Mapped[str] = mapped_column(String, nullable=True)
