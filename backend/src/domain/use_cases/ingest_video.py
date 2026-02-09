from src.domain.entities.video import Video
from src.domain.ports.video_repository import IVideoRepository
from src.domain.ports.message_queue import IMessageQueue

class IngestVideoUseCase:
    def __init__(self, video_repo: IVideoRepository, message_queue: IMessageQueue):
        self.video_repo = video_repo
        self.message_queue = message_queue

    async def execute(self, video_data: dict) -> Video:
        video = Video(**video_data)
        saved_video = await self.video_repo.save(video)

        # Publish task for processing (download audio, transcribe, etc.)
        await self.message_queue.publish_task(
            "process_video",
            {"video_id": saved_video.id, "url": str(saved_video.url)}
        )

        return saved_video
