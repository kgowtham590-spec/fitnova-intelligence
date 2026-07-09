import logging

logger = logging.getLogger(__name__)

class DiarizationService:
    def __init__(self):
        self.has_pipeline = False
        logger.info("Diarization Service initialized. Configured for fallback-first execution.")

    def diarize(self, audio_path: str, transcript_segments: list) -> list:
        diarized_segments = []
        for i, seg in enumerate(transcript_segments):
            speaker = seg.get("speaker", "Advisor" if i % 2 == 0 else "Customer")
            diarized_segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "speaker": speaker,
                "text": seg["text"]
            })
        return diarized_segments
