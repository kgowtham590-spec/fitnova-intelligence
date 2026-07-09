import logging

logger = logging.getLogger(__name__)


class DiarizationService:
    def __init__(self):
        logger.info("Using simple rule-based diarization.")

    def diarize(self, audio_path: str, transcript_segments: list) -> list:
        diarized_segments = []

        current_speaker = "Advisor"

        for i, seg in enumerate(transcript_segments):

            if i > 0:
                previous = transcript_segments[i - 1]

                # Switch speaker after long pause
                if seg["start"] - previous["end"] > 1.0:
                    current_speaker = (
                        "Customer"
                        if current_speaker == "Advisor"
                        else "Advisor"
                    )

                # Switch speaker for short replies
                elif len(seg["text"].split()) <= 3:
                    current_speaker = (
                        "Customer"
                        if current_speaker == "Advisor"
                        else "Advisor"
                    )

            diarized_segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "speaker": current_speaker,
                "text": seg["text"]
            })

        logger.info(f"Diarized {len(diarized_segments)} segments.")

        return diarized_segments
