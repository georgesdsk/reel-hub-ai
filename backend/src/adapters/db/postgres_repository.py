from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.video import Video
from src.domain.ports.video_repository import IVideoRepository
from src.adapters.db.models import VideoModel

class PostgresRepository(IVideoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, video: Video) -> Video:
        model = VideoModel(
            id=video.id,
            url=str(video.url),
            title=video.title,
            thumbnail=str(video.thumbnail) if video.thumbnail else None,
            transcript=video.transcript,
            tags=video.tags,
            category=video.category,
            ingredients=video.ingredients,
            steps=video.steps,
            duration=video.duration,
            source=video.source,
            saved_at=video.saved_at,
            user_note=video.user_note,
            embedding=video.embedding,
            language=video.language
        )

        # Check if exists to update
        existing = await self.session.get(VideoModel, video.id)
        if existing:
            for key, value in model.__dict__.items():
                if not key.startswith('_'):
                    setattr(existing, key, value)
        else:
            self.session.add(model)

        await self.session.commit()
        return video

    async def get_by_id(self, video_id: str) -> Optional[Video]:
        result = await self.session.execute(select(VideoModel).where(VideoModel.id == video_id))
        model = result.scalar_one_or_none()
        if model:
            return self._to_entity(model)
        return None

    async def search(self, query_embedding: List[float], limit: int = 10) -> List[Video]:
        result = await self.session.execute(
            select(VideoModel)
            .order_by(VideoModel.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def list_all(self, category: Optional[str] = None) -> List[Video]:
        query = select(VideoModel)
        if category:
            query = query.where(VideoModel.category == category)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: VideoModel) -> Video:
        return Video(
            id=model.id,
            url=model.url,
            title=model.title,
            thumbnail=model.thumbnail,
            transcript=model.transcript,
            tags=model.tags,
            category=model.category,
            ingredients=model.ingredients,
            steps=model.steps,
            duration=model.duration,
            source=model.source,
            saved_at=model.saved_at,
            user_note=model.user_note,
            embedding=model.embedding.tolist() if model.embedding is not None else None,
            language=model.language
        )
