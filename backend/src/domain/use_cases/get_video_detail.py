from typing import Optional
from src.domain.entities.video import Video
from src.domain.ports.video_repository import IVideoRepository

class GetVideoDetailUseCase:
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    async def execute(self, video_id: str) -> Optional[Video]:
        return await self.video_repo.get_by_id(video_id)
