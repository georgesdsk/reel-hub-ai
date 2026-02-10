from typing import List, Optional, Dict
from sqlalchemy import select, func, or_, desc, asc, text, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.video import Video
from src.domain.ports.video_repository import IVideoRepository
from src.adapters.db.models import VideoModel
from datetime import datetime, timezone, timedelta

class PostgresVideoRepository(IVideoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, video: Video) -> Video:
        # Check if exists to update
        existing_model = await self.session.get(VideoModel, video.id)

        if existing_model:
            # Update existing
            existing_model.url = str(video.url)
            existing_model.title = video.title
            existing_model.thumbnail = str(video.thumbnail) if video.thumbnail else None
            existing_model.transcript = video.transcript
            existing_model.tags = video.tags
            existing_model.category = video.category
            existing_model.ingredients = video.ingredients
            existing_model.steps = video.steps
            existing_model.duration = video.duration
            existing_model.source = video.source
            existing_model.saved_at = video.saved_at
            existing_model.user_note = video.user_note
            existing_model.embedding = video.embedding
            existing_model.language = video.language
            existing_model.telegram_user_id = video.telegram_user_id
            existing_model.processing_status = video.processing_status
            existing_model.job_id = video.job_id
            existing_model.error_message = video.error_message
            existing_model.processed_at = video.processed_at
        else:
            # Create new
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
                language=video.language,
                telegram_user_id=video.telegram_user_id,
                processing_status=video.processing_status,
                job_id=video.job_id,
                error_message=video.error_message,
                processed_at=video.processed_at
            )
            self.session.add(model)

        await self.session.commit()
        return video

    async def get_by_id(self, video_id: str) -> Optional[Video]:
        result = await self.session.execute(select(VideoModel).where(VideoModel.id == video_id))
        model = result.scalar_one_or_none()
        if model:
            return self._to_entity(model)
        return None

    async def get_by_url(self, url: str, telegram_user_id: Optional[int] = None) -> Optional[Video]:
        query = select(VideoModel).where(VideoModel.url == url)
        if telegram_user_id:
            query = query.where(VideoModel.telegram_user_id == telegram_user_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model:
            return self._to_entity(model)
        return None

    async def search_by_embedding(
        self,
        query_embedding: List[float],
        limit: int = 10,
        category: Optional[str] = None,
        telegram_user_id: Optional[int] = None
    ) -> List[Video]:
        # Using cosine distance for similarity
        query = select(VideoModel)

        if category:
            query = query.where(VideoModel.category == category)
        if telegram_user_id:
            query = query.where(VideoModel.telegram_user_id == telegram_user_id)

        query = query.order_by(VideoModel.embedding.cosine_distance(query_embedding)).limit(limit)

        result = await self.session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(m) for m in models]

    async def list(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        sort_by: str = "saved_at",
        order: str = "desc",
        telegram_user_id: Optional[int] = None
    ) -> List[Video]:
        query = select(VideoModel)

        if category:
            query = query.where(VideoModel.category == category)
        if telegram_user_id:
            query = query.where(VideoModel.telegram_user_id == telegram_user_id)
        if tags:
            for tag in tags:
                query = query.where(VideoModel.tags.contains([tag]))
        if search:
            query = query.where(
                or_(
                    VideoModel.title.ilike(f"%{search}%"),
                    VideoModel.transcript.ilike(f"%{search}%"),
                    VideoModel.user_note.ilike(f"%{search}%")
                )
            )

        sort_attr = getattr(VideoModel, sort_by, VideoModel.saved_at)
        if order == "desc":
            query = query.order_by(desc(sort_attr))
        else:
            query = query.order_by(asc(sort_attr))

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def count(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        telegram_user_id: Optional[int] = None
    ) -> int:
        query = select(func.count()).select_from(VideoModel)

        if category:
            query = query.where(VideoModel.category == category)
        if telegram_user_id:
            query = query.where(VideoModel.telegram_user_id == telegram_user_id)
        if tags:
            for tag in tags:
                query = query.where(VideoModel.tags.contains([tag]))
        if search:
            query = query.where(
                or_(
                    VideoModel.title.ilike(f"%{search}%"),
                    VideoModel.transcript.ilike(f"%{search}%"),
                    VideoModel.user_note.ilike(f"%{search}%")
                )
            )

        result = await self.session.execute(query)
        return result.scalar()

    async def delete(self, video_id: str) -> bool:
        result = await self.session.execute(delete(VideoModel).where(VideoModel.id == video_id))
        await self.session.commit()
        return result.rowcount > 0

    async def get_statistics(self, telegram_user_id: Optional[int] = None) -> Dict:
        # Simplified for now
        total_query = select(func.count()).select_from(VideoModel)
        if telegram_user_id:
            total_query = total_query.where(VideoModel.telegram_user_id == telegram_user_id)

        total_result = await self.session.execute(total_query)
        total_videos = total_result.scalar()

        last_month = datetime.now(timezone.utc) - timedelta(days=30)
        month_query = select(func.count()).select_from(VideoModel).where(VideoModel.saved_at >= last_month)
        if telegram_user_id:
            month_query = month_query.where(VideoModel.telegram_user_id == telegram_user_id)

        month_result = await self.session.execute(month_query)
        videos_last_month = month_result.scalar()

        return {
            "total_videos": total_videos,
            "by_category": {},
            "by_source": {},
            "videos_last_month": videos_last_month
        }

    async def get_categories_with_count(self, telegram_user_id: Optional[int] = None) -> List[Dict]:
        query = select(VideoModel.category, func.count()).group_by(VideoModel.category)
        if telegram_user_id:
            query = query.where(VideoModel.telegram_user_id == telegram_user_id)

        result = await self.session.execute(query)
        return [{"name": str(row[0]), "count": row[1]} for row in result.all()]

    async def get_popular_tags(self, limit: int = 50, telegram_user_id: Optional[int] = None) -> List[Dict]:
        tag_func = func.unnest(VideoModel.tags).label("tag")
        query = select(tag_func, func.count()).group_by("tag").order_by(desc(func.count())).limit(limit)
        if telegram_user_id:
            query = query.where(VideoModel.telegram_user_id == telegram_user_id)
        result = await self.session.execute(query)
        return [{"tag": row[0], "count": row[1]} for row in result.all()]

    async def get_tags_matching(self, q: str, limit: int = 5) -> List[str]:
        tag_func = func.unnest(VideoModel.tags).label("tag")
        query = select(tag_func).distinct().where(tag_func.ilike(f"%{q}%")).limit(limit)
        result = await self.session.execute(query)
        return [row[0] for row in result.all()]

    async def get_titles_matching(self, q: str, limit: int = 5) -> List[str]:
        query = select(VideoModel.title).where(VideoModel.title.ilike(f"%{q}%")).limit(limit)
        result = await self.session.execute(query)
        return [row[0] for row in result.all()]

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
            language=model.language,
            telegram_user_id=model.telegram_user_id,
            processing_status=model.processing_status,
            job_id=model.job_id,
            error_message=model.error_message,
            processed_at=model.processed_at
        )
