from celery import Task
from src.adapters.queue.celery_app import celery_app
import logging
import asyncio
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class CallbackTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True

@celery_app.task(bind=True, base=CallbackTask, name='tasks.process_video')
def process_video_task(self, video_id: str):
    from src.adapters.media.downloader import MediaDownloader
    from src.adapters.ai.whisper_adapter import WhisperAdapter
    from src.adapters.ai.embeddings_adapter import EmbeddingsAdapter
    from src.adapters.ai.categorizer_adapter import CategorizerAdapter
    from src.adapters.db.postgres_repository import PostgresVideoRepository
    from src.adapters.db.connection import async_session
    from src.config.settings import settings

    async def _process():
        async with async_session() as session:
            repo = PostgresVideoRepository(session)
            video = await repo.get_by_id(video_id)
            if not video or video.processing_status == "completed": return
            video.processing_status = "processing"
            video.job_id = self.request.id
            await repo.save(video)
            audio_path = None
            downloader = MediaDownloader(temp_dir=settings.TEMP_DIR)
            try:
                audio_path, metadata = await downloader.download_audio(str(video.url), video.source)
                video.title = metadata.get("title", video.title)
                video.duration = metadata.get("duration", video.duration)
                video.thumbnail = metadata.get("thumbnail", video.thumbnail)
                whisper = WhisperAdapter(model_size=settings.WHISPER_MODEL_SIZE)
                transcription = await whisper.transcribe(audio_path)
                video.transcript = transcription["text"]
                video.language = transcription["language"]
                categorizer = CategorizerAdapter(api_key=settings.GROQ_API_KEY)
                category_result = await categorizer.categorize(video.transcript, video.title, video.language)
                video.category = category_result["category"]
                video.tags = category_result["tags"]
                video.ingredients = category_result.get("ingredients", [])
                video.steps = category_result.get("steps", [])
                embeddings = EmbeddingsAdapter(model_name=settings.EMBEDDING_MODEL)
                video.embedding = await embeddings.generate_embedding(video.transcript or video.title or "")
                video.processing_status = "completed"
                video.processed_at = datetime.now(timezone.utc)
                await repo.save(video)
                return {"status": "success", "video_id": video_id}
            except Exception as e:
                video.processing_status = "failed"
                video.error_message = str(e)
                await repo.save(video)
                raise e
            finally:
                if audio_path: downloader.cleanup(audio_path)
    return asyncio.run(_process())

@celery_app.task(name='tasks.batch_import_videos')
def batch_import_videos_task(urls_data: list[dict]):
    from src.adapters.db.postgres_repository import PostgresVideoRepository
    from src.adapters.db.connection import async_session
    from src.domain.use_cases.ingest_video import IngestVideoUseCase
    async def _batch_import():
        async with async_session() as session:
            repo = PostgresVideoRepository(session)
            ingest_uc = IngestVideoUseCase(repo)
            for item in urls_data:
                try:
                    video = await ingest_uc.execute(url=item['url'], source=item['source'], user_note=item.get('user_note'), telegram_user_id=item.get('telegram_user_id'))
                    process_video_task.delay(video.id)
                except: pass
            return {"total": len(urls_data)}
    return asyncio.run(_batch_import())
