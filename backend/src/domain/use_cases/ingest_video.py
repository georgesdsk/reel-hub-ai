from src.domain.entities.video import Video, VideoSource
from src.domain.ports.video_repository import IVideoRepository
from typing import Optional

class IngestVideoUseCase:
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    async def execute(
        self,
        url: str,
        source: VideoSource,
        user_note: Optional[str] = None,
        telegram_user_id: Optional[int] = None
    ) -> Video:
        # Check if already exists for this user
        existing_video = await self.video_repo.get_by_url(url, telegram_user_id=telegram_user_id)
        if existing_video:
            return existing_video

        video = Video(
            url=url,
            source=source,
            user_note=user_note,
            telegram_user_id=telegram_user_id,
            processing_status="pending"
        )
        saved_video = await self.video_repo.save(video)
        return saved_video
