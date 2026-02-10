from typing import List, Optional
from src.domain.entities.video import Video
from src.domain.ports.video_repository import IVideoRepository

class SearchVideosUseCase:
    def __init__(
        self,
        repository: IVideoRepository,
        embeddings_adapter = None
    ):
        self.repository = repository
        self.embeddings = embeddings_adapter

    async def execute(
        self,
        query_embedding: Optional[List[float]] = None,
        query_text: Optional[str] = None,
        limit: int = 20,
        category: Optional[str] = None,
        telegram_user_id: Optional[int] = None
    ) -> List[Video]:
        """
        Búsqueda híbrida: semántica + filtros.
        """
        if query_text and not query_embedding and self.embeddings:
            query_embedding = await self.embeddings.generate_embedding(query_text)

        if not query_embedding:
            if query_text:
                return await self.repository.list(
                    limit=limit,
                    category=category,
                    search=query_text,
                    telegram_user_id=telegram_user_id
                )
            raise ValueError("Either query_embedding or query_text (with embeddings_adapter) is required")

        # Search en DB
        videos = await self.repository.search_by_embedding(
            query_embedding=query_embedding,
            limit=limit,
            category=category,
            telegram_user_id=telegram_user_id
        )

        return videos
