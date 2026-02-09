import pytest
from unittest.mock import AsyncMock, MagicMock
from src.domain.use_cases.ingest_video import IngestVideoUseCase
from src.domain.entities.video import Video
from src.domain.entities.enums import VideoSource

@pytest.mark.asyncio
async def test_ingest_video_use_case():
    video_repo = AsyncMock()
    message_queue = AsyncMock()

    use_case = IngestVideoUseCase(video_repo, message_queue)

    video_data = {
        "url": "https://instagram.com/reel/123",
        "source": VideoSource.INSTAGRAM
    }

    video_repo.save.side_effect = lambda v: v

    result = await use_case.execute(video_data)

    assert str(result.url).rstrip('/') == "https://instagram.com/reel/123"
    video_repo.save.assert_called_once()
    message_queue.publish_task.assert_called_once()
