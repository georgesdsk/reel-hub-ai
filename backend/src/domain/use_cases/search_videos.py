from typing import List
from src.domain.entities.video import Video
from src.domain.ports.video_repository import IVideoRepository
from src.domain.ports.ai_service import IAIService

class SearchVideosUseCase:
    def __init__(self, video_repo: IVideoRepository, ai_service: IAIService):
        self.video_repo = video_repo
        self.ai_service = ai_service

    async def execute(self, query: str) -> List[Video]:
        query_embedding = await self.ai_service.generate_embedding(query)
        return await self.video_repo.search(query_embedding)
