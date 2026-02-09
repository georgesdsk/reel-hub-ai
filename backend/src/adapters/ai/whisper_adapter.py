from faster_whisper import WhisperModel
import logging
logger = logging.getLogger(__name__)

class WhisperAdapter:
    def __init__(self, model_size="base", device="cpu"):
        try: self.model = WhisperModel(model_size, device=device, compute_type="int8")
        except: self.model = None
    async def transcribe(self, audio_path, language=None):
        if not self.model: return {"text": "Transcription placeholder", "language": "es"}
        segments, info = self.model.transcribe(str(audio_path), language=language)
        return {"text": " ".join([s.text for s in segments]), "language": info.language}
