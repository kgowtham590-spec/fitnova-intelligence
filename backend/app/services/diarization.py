import logging
import os

from app.core.config import settings

logger = logging.getLogger(__name__)


class DiarizationService:
    def __init__(self):
        self.hf_token = settings.HF_TOKEN
        self.pipeline = None
        self.has_pipeline = False

        if not self.hf_token:
            logger.warning(
                "HF_TOKEN not found. Speaker diarization disabled. Falling back to heuristic diarization."
            )
            return

        try:
            from pyannote.audio import Pipeline

            logger.info("Loading Pyannote Speaker Diarization pipeline...")

            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.hf_token,
            )

            self.has_pipeline = True
            logger.info("Pyannote Speaker Diarization loaded successfully.")

        except ImportError:
            logger.exception(
                "pyannote.audio is not installed. Falling back to heuristic diarization."
            )

        except Exception as e:
            logger.exception(
                f"Failed to load Pyannote pipeline: {e}. Falling back to heuristic diarization."
            )

    def diarize(self, audio_path: str, transcript_segments: list) -> list:
        diarized_segments = []

        if self.has_pipeline and audio_path and os.path.exists(audio_path):
            try:
                logger.info(f"Running speaker diarization on {audio_path}")

                annotation = self.pipeline(audio_path)

                pyannote_turns = []

                for turn, _, speaker in annotation.itertracks(yield_label=True):
                    pyannote_turns.append(
                        {
                            "start": turn.start,
                            "end": turn.end,
                            "speaker": speaker,
                        }
                    )

                logger.info(
                    f"Pyannote detected {len(pyannote_turns)} speaker turns."
                )

                if pyannote_turns:
                    diarized_segments = self._merge_whisper_and_pyannote(
                        transcript_segments,
                        pyannote_turns,
                    )
                else:
                    logger.warning(
                        "No speaker turns returned by Pyannote. Using heuristic diarization."
                    )
                    diarized_segments = self._heuristic_diarize(
                        transcript_segments
                    )

            except Exception as e:
                logger.exception(
                    f"Speaker diarization failed: {e}. Using heuristic diarization."
                )
                diarized_segments = self._heuristic_diarize(
                    transcript_segments
                )

        else:
            diarized_segments = self._heuristic_diarize(transcript_segments)

        return self._clean_and_merge(diarized_segments)

    def _merge_whisper_and_pyannote(
        self,
        whisper_segments: list,
        pyannote_turns: list,
    ) -> list:

        raw_segments = []

        for seg in whisper_segments:
            w_start = seg["start"]
            w_end = seg["end"]

            overlaps = {}

            for turn in pyannote_turns:
                overlap_start = max(w_start, turn["start"])
                overlap_end = min(w_end, turn["end"])

                overlap = max(0.0, overlap_end - overlap_start)

                if overlap > 0:
                    speaker = turn["speaker"]
                    overlaps[speaker] = overlaps.get(speaker, 0) + overlap

            if overlaps:
                speaker = max(overlaps, key=overlaps.get)
            else:
                speaker = pyannote_turns[0]["speaker"]

            raw_segments.append(
                {
                    "start": w_start,
                    "end": w_end,
                    "text": seg["text"],
                    "raw_speaker": speaker,
                }
            )

        advisor_keywords = [
            "fitnova",
            "thank you for calling",
            "how can i help",
            "my name is",
            "free trial",
            "coaching",
            "membership",
            "subscription",
            "trainer",
            "plan",
            "amit",
            "priya",
            "rohan",
        ]

        speaker_scores = {}

        for seg in raw_segments:
            score = 0

            text = seg["text"].lower()

            for keyword in advisor_keywords:
                if keyword in text:
                    score += 1

            if score:
                speaker_scores[seg["raw_speaker"]] = (
                    speaker_scores.get(seg["raw_speaker"], 0)
                    + score
                )

        advisor_speaker = None

        if speaker_scores:
            advisor_speaker = max(
                speaker_scores,
                key=speaker_scores.get,
            )
        elif raw_segments:
            advisor_speaker = raw_segments[0]["raw_speaker"]

        diarized = []

        for seg in raw_segments:
            diarized.append(
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": (
                        "Advisor"
                        if seg["raw_speaker"] == advisor_speaker
                        else "Customer"
                    ),
                    "text": seg["text"],
                }
            )

        return diarized

    def _heuristic_diarize(self, transcript_segments: list) -> list:
        diarized = []

        for i, seg in enumerate(transcript_segments):
            diarized.append(
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": (
                        seg.get("speaker")
                        or ("Advisor" if i % 2 == 0 else "Customer")
                    ),
                    "text": seg["text"],
                }
            )

        return diarized

    def _clean_and_merge(self, segments: list) -> list:
        cleaned = []

        for seg in segments:
            text = seg.get("text", "").strip()

            if not text:
                continue

            cleaned.append(
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": seg["speaker"],
                    "text": text,
                }
            )

        if not cleaned:
            return []

        merged = []

        current = cleaned[0]

        for nxt in cleaned[1:]:

            if nxt["speaker"] == current["speaker"]:

                if nxt["text"].lower() == current["text"].lower():
                    current["end"] = nxt["end"]
                else:
                    current["text"] += " " + nxt["text"]
                    current["end"] = nxt["end"]

            else:
                merged.append(current)
                current = nxt

        merged.append(current)

        return merged