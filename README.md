# AI-Powered Customer Conversation Intelligence Platform

An end-to-end AI platform that turns raw customer sales-call recordings into structured business insights — transcription, speaker diarization, compliance detection, and an AI-driven quality evaluation, all surfaced through an interactive dashboard.

**Live demo:** [fitnova-intelligence-nine.vercel.app](https://fitnova-intelligence-nine.vercel.app/) · [Director Dashboard](https://fitnova-intelligence-nine.vercel.app/director)

![FitNova Dashboard](docs/screenshots/dashboard.png)

---

## Why This Project

Sales teams record thousands of calls but rarely have time to review them systematically. FitNova automates that review: upload a call, and within minutes get a transcript, a diarized conversation, a compliance check, a quality score across seven dimensions, and an executive summary with recommendations — the kind of analysis a manager would otherwise spend 20+ minutes doing manually per call.

---

## Architecture

```
Audio Upload
     │
     ▼
Groq Whisper Large v3  ──────────►  Transcript
     │
     ▼
PyAnnote Speaker Diarization  ───►  Speaker-labeled segments
     │
     ▼
Advisor / Customer Mapping
     │
     ▼
PII Redaction
     │
     ▼
LangGraph Evaluation Workflow
     ├── Discovery & Rapport Analysis
     ├── Product Knowledge Check
     ├── Objection Handling Review
     ├── Closing Technique Scoring
     ├── Compliance Flagging
     └── Executive Summary + Recommendations
     │
     ▼
SQLite Persistence
     │
     ▼
React Dashboard (scores, timeline, audio playback)
```

**Backend:** FastAPI · Python · SQLAlchemy · SQLite · Pydantic
**Frontend:** React · TypeScript · Vite · Tailwind CSS · Recharts · Axios
**AI:** Groq Whisper Large v3 · PyAnnote.audio 3.3 · LangGraph · Hugging Face

---

## How the AI Evaluation Works

The core of FitNova is a **LangGraph workflow** that takes the redacted, speaker-labeled transcript and runs it through a graph of evaluation nodes rather than a single monolithic prompt. Each node focuses on one dimension of the call:

| Node | What it evaluates |
|---|---|
| Discovery | Whether the advisor asked effective qualifying questions |
| Rapport | Tone, empathy, and relationship-building signals |
| Product Knowledge | Accuracy and depth of product/service explanations |
| Objection Handling | How customer pushback was addressed |
| Closing | Presence and quality of a clear next step / close |
| Compliance | Required disclosures, prohibited language, regulatory flags |
| Customer Experience | Overall sentiment and satisfaction signals |

Each node produces a structured score plus supporting rationale, which the graph then aggregates into an overall quality score, a set of compliance flags, and an LLM-generated executive summary with actionable recommendations.

*(Fill in: are these nodes sequential or parallel in your graph? Do you pass the full transcript to each node or a filtered segment? A sentence or two here — and ideally a small graph-diagram screenshot from LangGraph's visualizer — will make this section much stronger for reviewers.)*

---

## Features

- Upload sales call recordings
- Automatic speech-to-text transcription (Groq Whisper Large v3)
- Real speaker diarization (PyAnnote)
- Advisor / Customer speaker mapping
- PII redaction before evaluation
- AI-powered sales quality scoring across 7 dimensions
- Compliance issue detection
- AI-generated executive summary + recommendations
- Interactive dashboard with audio playback and conversation timeline
- REST API backend, SQLite storage

---

## Project Structure

```
fitnova-intelligence/
├── backend/
│   ├── app/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── schemas/
│   ├── services/
│   ├── requirements.txt
│   └── seed.py
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

Create a `.env`:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=whisper-large-v3
HF_TOKEN=your_huggingface_token
```

```bash
python seed.py
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key |
| `GROQ_MODEL` | Whisper model |
| `HF_TOKEN` | Hugging Face token for PyAnnote |

---

## Design Decisions & Trade-offs

| Choice | Reasoning | Trade-off accepted |
|---|---|---|
| SQLite over PostgreSQL | Simpler deployment for a prototype | Not suited for concurrent production write loads |
| Groq Whisper over local inference | High-quality transcription with low latency, no GPU needed | Dependent on external API availability/cost |
| Prompt-driven evaluation over custom ML models | Faster to build, easier to iterate on evaluation criteria | Less consistent than a fine-tuned classifier at scale |
| Heuristic Advisor/Customer mapping on PyAnnote diarization | Avoids need for labeled training data | Occasional mis-mapping on ambiguous calls |

---

## Known Limitations

- Speaker role mapping may occasionally assign Advisor/Customer incorrectly
- Very noisy recordings can reduce diarization accuracy
- AI evaluation quality is bounded by transcription accuracy
- Only supports uploaded recordings (no live call processing)

## Future Improvements

- Real-time call analysis
- CRM integration
- Multi-language transcription
- Team performance analytics
- Authentication & multi-tenant support
- PostgreSQL + vector database for semantic search / RAG over past calls
- Improved speaker role classification

---

## Deployment

- **Frontend:** [fitnova-intelligence-nine.vercel.app](https://fitnova-intelligence-nine.vercel.app/)
- **Director Dashboard:** [fitnova-intelligence-nine.vercel.app/director](https://fitnova-intelligence-nine.vercel.app/director)
- **Backend API:** [fitnova-backend-h4uh.onrender.com](https://fitnova-backend-h4uh.onrender.com)

> Note: the backend is on Render's free tier, which cold-starts after inactivity. If you're sharing this link during a screening call, hit the API once beforehand to warm it up.

---

## Author

**Gowtham K**
[GitHub](https://github.com/kgowtham590-spec)

## License

Developed as an internship prototype for educational and demonstration purposes.
