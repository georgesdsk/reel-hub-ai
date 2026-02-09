from src.domain.ports.video_repository import IVideoRepository
from src.domain.ports.ai_service import IAIService

class TranscribeVideoUseCase:
    def __init__(self, video_repo: IVideoRepository, ai_service: IAIService):
        self.video_repo = video_repo
        self.ai_service = ai_service

    async def execute(self, video_id: str, audio_path: str):
        video = await self.video_repo.get_by_id(video_id)
        if not video:
            raise ValueError(f"Video with id {video_id} not found")

        transcript = await self.ai_service.transcribe(audio_path)
        ai_analysis = await self.ai_service.categorize(transcript)
        embedding = await self.ai_service.generate_embedding(transcript)

        video.transcript = transcript
        video.category = ai_analysis.get("category", video.category)
        video.tags = ai_analysis.get("tags", [])
        video.ingredients = ai_analysis.get("ingredients", [])
        video.steps = ai_analysis.get("steps", [])
        video.embedding = embedding

        await self.video_repo.save(video)
        return video
