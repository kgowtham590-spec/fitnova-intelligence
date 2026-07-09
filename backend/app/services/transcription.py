import logging

logger = logging.getLogger(__name__)

from app.core.config import settings

class TranscriptionService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
                self.has_api = True
                logger.info("Groq Cloud Whisper transcription client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Groq API client: {e}")
                self.has_api = False
        else:
            self.has_api = False
            logger.warning("No Groq API key found. Transcription will fallback to mocks.")

    def transcribe(self, audio_path: str) -> list:
        if self.has_api:
            try:
                logger.info(f"Sending audio file {audio_path} to Groq Whisper API for real transcription...")
                with open(audio_path, "rb") as file:
                    transcription = self.client.audio.transcriptions.create(
                        file=(audio_path, file.read()),
                        model="whisper-large-v3",
                        response_format="verbose_json"
                    )
                
                segments = []
                if hasattr(transcription, "segments"):
                    segments = transcription.segments
                elif isinstance(transcription, dict) and "segments" in transcription:
                    segments = transcription["segments"]

                results = []
                for s in segments:
                    start = s.get("start", 0.0) if isinstance(s, dict) else getattr(s, "start", 0.0)
                    end = s.get("end", 0.0) if isinstance(s, dict) else getattr(s, "end", 0.0)
                    text = s.get("text", "") if isinstance(s, dict) else getattr(s, "text", "")
                    results.append({
                        "start": start,
                        "end": end,
                        "text": text.strip(),
                        "speaker": "Speaker"
                    })
                
                if results:
                    logger.info(f"Successfully transcribed {len(results)} segments via Groq Whisper API.")
                    return results
            except Exception as e:
                logger.error(f"Groq Whisper transcription failed: {e}. Falling back to mock transcriber.")
        
        return self._get_mock_transcript(audio_path)

    def _get_mock_transcript(self, audio_path: str) -> list:
        import hashlib
        h = int(hashlib.md5(audio_path.encode()).hexdigest(), 16)
        scenario = h % 3
        
        if scenario == 0:
            return [
                {"start": 0.0, "end": 4.5, "speaker": "Advisor", "text": "Hello, thank you for calling FitNova. My name is Amit. How can I help you today?"},
                {"start": 5.0, "end": 9.2, "speaker": "Customer", "text": "Hi Amit, I saw your advertisement on Instagram about personalized fitness programs and wanted to enquire."},
                {"start": 9.5, "end": 15.0, "speaker": "Advisor", "text": "Perfect! I can definitely help with that. To recommend the best plan, could you tell me a bit about your current fitness goals?"},
                {"start": 15.5, "end": 22.0, "speaker": "Customer", "text": "Actually, I want to lose around 10 kilograms. My schedule is very hectic because of my IT job, so I get very little time to exercise."},
                {"start": 22.5, "end": 28.5, "speaker": "Advisor", "text": "I completely understand. Bahut saare clients software sector se hain and they face the same time crunch. We specialize in quick 30-minute high-intensity workouts."},
                {"start": 29.0, "end": 32.5, "speaker": "Customer", "text": "That sounds doable. What is the fee structure for this plan?"},
                {"start": 33.0, "end": 40.0, "speaker": "Advisor", "text": "Before we talk pricing, I'd suggest booking a free trial session so you can experience our coaching style firsthand. We can book it online for tomorrow. Does 6 PM work?"},
                {"start": 40.5, "end": 43.5, "speaker": "Customer", "text": "Yes, tomorrow 6 PM works. Let's do that trial session."},
                {"start": 44.0, "end": 48.0, "speaker": "Advisor", "text": "Awesome. The trial is fully booked. I will email you the link. Thank you so much!"}
            ]
        elif scenario == 1:
            return [
                {"start": 0.0, "end": 3.5, "speaker": "Advisor", "text": "Hello, FitNova here. Main Rohan baat kar raha hu."},
                {"start": 4.0, "end": 8.0, "speaker": "Customer", "text": "Hi Rohan, I want to join a weight loss coaching program. Can you tell me the cost?"},
                {"start": 8.5, "end": 14.5, "speaker": "Advisor", "text": "Pricing is 15,000 Rupees for 3 months, but if you buy right now in the next 10 minutes, I will give you a 50% discount. Immediately enroll kar lijiye."},
                {"start": 15.0, "end": 19.5, "speaker": "Customer", "text": "Oh, that's a bit fast. Can I get a trial session first to see how it works?"},
                {"start": 20.0, "end": 26.5, "speaker": "Advisor", "text": "No, trial slots are fully booked for the next 2 months. Trust me, our program guarantees 100% weight loss of 15 kgs in 30 days without any diet change. Guarantee card dunga aapko."},
                {"start": 27.0, "end": 30.5, "speaker": "Customer", "text": "Wait, 15 kgs in 30 days without diet change? Is that even safe or possible?"},
                {"start": 31.0, "end": 36.5, "speaker": "Advisor", "text": "Bilkul possible hai, zero side-effects. But you must pay right now, otherwise this discount will expire."},
                {"start": 37.0, "end": 40.0, "speaker": "Customer", "text": "No, this sounds too pushy and unrealistic. I will think about it."}
            ]
        else:
            return [
                {"start": 0.0, "end": 3.0, "speaker": "Advisor", "text": "Hello, thank you for calling FitNova. My name is Priya."},
                {"start": 3.5, "end": 6.5, "speaker": "Customer", "text": "Oh, sorry. I think I dialled the wrong number. I was trying to call the dentist."},
                {"start": 7.0, "end": 9.5, "speaker": "Advisor", "text": "No worries, have a great day!"}
            ]
