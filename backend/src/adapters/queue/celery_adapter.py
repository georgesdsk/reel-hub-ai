from celery.result import AsyncResult
from src.domain.ports.message_queue import IMessageQueue
from src.adapters.queue.celery_app import celery_app
from src.adapters.queue.tasks import process_video_task

class CeleryMessageQueue(IMessageQueue):
    async def enqueue(self, video_id: str) -> str:
        result = process_video_task.delay(video_id)
        return result.id

    async def get_status(self, job_id: str) -> dict:
        result = AsyncResult(job_id, app=celery_app)
        return {
            "job_id": job_id,
            "status": result.state,
            "progress": result.info if isinstance(result.info, dict) else {},
            "result": result.result if result.ready() else None
        }

    async def cancel(self, job_id: str) -> bool:
        celery_app.control.revoke(job_id, terminate=True)
        return True

    async def enqueue_batch(self, videos_data: list[dict]) -> str:
        from src.adapters.queue.tasks import batch_import_videos_task
        result = batch_import_videos_task.delay(videos_data)
        return result.id

    async def get_batch_status(self, job_id: str) -> dict:
        result = AsyncResult(job_id, app=celery_app)
        return {
            "job_id": job_id,
            "status": result.state,
            "progress": result.info if isinstance(result.info, dict) else {"processed": 0, "total": 0},
            "urls_processed": [],
            "errors": []
        }
