# FitNova AI Sales-Call Intelligence System

> **AI Engineer Intern Take-Home Assignment — FitNova Bangalore**

An end-to-end AI-powered Sales-Call Intelligence System that automatically ingests call recordings, transcribes audio, performs speaker diarization, redacts PII, scores advisor quality, detects compliance issues, and surfaces everything via role-aware dashboards for the Sales Director, Team Leaders, and individual Advisors.

---

## 🚀 Quick Start (Single Command)

**Windows** — double-click or run in PowerShell:
```bat
start.bat
```
This will: install all dependencies, seed the database with 3 sample processed calls, start the FastAPI backend (`port 8000`) and the Vite React frontend (`port 3000`), and open the browser automatically.

**Manual start** (if you prefer separate terminals):
```bash
# Terminal 1 – Backend
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 – Frontend
cd frontend
npm run dev
```
Open **http://localhost:3000**

---

## 🏗️ Architecture

See the full pipeline diagram and written walkthrough: [`docs/architecture.md`](docs/architecture.md)

```
[Ingestion] → [Transcription + Diarization] → [PII Redaction]
    → [Analysis Engine (Score + Issue + Summary Agents)]
        → [SQLite Storage]
            → [React Dashboards]
                → [Advisor Appeals → TL Review → Resolve]
```

**Source-agnostic ingestion**: `FolderConnector`, `TwilioConnector`, `CRMConnector`, and `UploadConnector` all implement `AbstractConnector` — adding a new telephony vendor requires only one new class, zero changes to the pipeline.

---

## 📦 Components

| Layer | Tech | Purpose |
|---|---|---|
| Backend API | FastAPI + SQLAlchemy | Upload, analysis, scoring, appeals, analytics |
| Database | SQLite (→ PostgreSQL via env var) | Orgs, Teams, Advisors, Calls, Scores, Issues, Appeals, Logs |
| Analysis Engine | LLM (OpenAI) + heuristic fallback | 7-dimension scoring, 8 issue types, hallucination guard |
| Transcription | Faster-Whisper + mock fallback | Audio → labeled transcript segments |
| Diarization | pyannote.audio + mock fallback | Advisor vs Customer speaker separation |
| PII Redaction | Regex (phone, email, UPI, card, address) | Redacted text stored alongside raw |
| Frontend | React + Vite + TailwindCSS + Recharts | Director / TL / Advisor dashboards |

---

## 🔑 What Is Real vs. Mocked

| Feature | Real | Mocked / Fallback |
|---|---|---|
| FastAPI REST API | ✅ | — |
| SQLite relational storage | ✅ | — |
| PII Redaction | ✅ | — |
| LLM scoring (OpenAI GPT) | ✅ with `OPENAI_API_KEY` | Heuristic rules (deterministic) |
| Hallucination guard (quote verification) | ✅ | ✅ same logic |
| Whisper transcription | ✅ with `faster-whisper` installed | Realistic scenario transcripts |
| Speaker diarization | ✅ with `pyannote.audio` + `HF_TOKEN` | Mock speaker labels |
| Appeals workflow | ✅ | — |
| React dashboards | ✅ | — |

**The system is fully testable without any API keys.** The mock pipeline produces three distinct scenarios: a model discovery call (Amit), a high-pressure non-compliant call (Rohan), and a wrong-number call (Priya) — all with realistic transcripts, scores, and issue flags.

---

## 🌍 Environment Variables

Create `backend/.env`:
```env
# Optional — if not set, mock pipeline is used
OPENAI_API_KEY=your_openai_key_here
HF_TOKEN=your_huggingface_token_here

# Optional — defaults to sqlite in backend dir
DATABASE_URL=sqlite:///./fitnova.db

# Optional
UPLOAD_DIR=./data/uploads
```

---

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | System health |
| POST | `/api/v1/upload` | Upload a new call recording |
| GET | `/api/v1/calls` | List calls (filters: team, advisor, status, score) |
| GET | `/api/v1/calls/{id}` | Call detail (transcript, scores, issues) |
| GET | `/api/v1/org/structure` | Org → Teams → Advisors |
| GET | `/api/v1/org/analytics` | Score averages, team rankings, issue breakdown |
| POST | `/api/v1/appeals` | Advisor submits appeal on an issue |
| GET | `/api/v1/appeals` | List all appeals |
| PUT | `/api/v1/appeals/{id}` | TL approves/rejects appeal |

---

## 🧪 Edge Cases Handled

- **Mono / poor diarization** → mock fallback, no crash
- **Hindi-English code-switching** → Whisper multilingual; mock transcripts include Hindi phrases
- **Non-sales call (wrong number)** → detected and scored appropriately (all sales dimensions → 0)
- **PII** → redacted before storage; both raw and redacted versions preserved
- **Hallucinated issue flags** → quote must exist verbatim in transcript or flag is rejected
- **LLM API failure** → immediate fallback to heuristic analysis
- **Vendor switch** → add one new `AbstractConnector` subclass

---

## 📁 Project Structure

```
fitnova-intelligence/
├── start.bat                    ← Single-command startup
├── README.md
├── docs/
│   ├── architecture.md          ← Full pipeline diagram + walkthrough
│   └── video_script.md          ← 2-minute video walkthrough script
├── backend/
│   ├── seed.py                  ← DB seeder (3 sample calls)
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── agents/              ← LLM analysis (score, issues, summary, hallucination guard)
│       ├── api/routes/          ← calls, upload, appeals, org
│       ├── core/                ← config, logging
│       ├── database/            ← models (9 tables), session
│       ├── ingestion/           ← AbstractConnector + Folder/Twilio/CRM connectors
│       ├── schemas/             ← Pydantic v2 request/response models
│       └── services/            ← transcription, diarization, PII redaction
└── frontend/
    └── src/
        └── pages/               ← SalesDirector, TeamLeader, Advisor, CallDetail, Analytics, Appeals
```

---

## 🎥 Video Walkthrough

See `docs/video_script.md` for the 2-minute walkthrough script.
Record and upload to an accessible link (YouTube unlisted / Loom) before submission.
