# FitNova AI Sales Call Intelligence Prototype

## Overview

FitNova AI Sales Call Intelligence is an end-to-end AI-powered application that analyzes customer sales calls and provides actionable insights for sales managers.

The application accepts an uploaded call recording, generates a transcript using Groq Whisper, identifies speakers, redacts sensitive information, evaluates the conversation using an AI workflow, stores the processed results in a database, and displays insights through an interactive dashboard.

This project was developed as a working prototype to demonstrate an AI-driven sales call intelligence pipeline.

---

# Features

- Upload customer sales call recordings
- Automatic speech-to-text transcription using Groq Whisper Large v3
- Advisor and Customer speaker identification
- Automatic PII (Personally Identifiable Information) redaction
- AI-powered call analysis
- Sales quality scoring
- Compliance issue detection
- AI-generated call summary
- AI-generated recommendations
- Interactive dashboard
- Database storage for processed calls

---

# Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router
- Recharts

## Backend

- FastAPI
- Python
- SQLAlchemy
- SQLite
- Pydantic

## AI Components

- Groq Whisper Large v3 (Speech Transcription)
- LangGraph-based AI Analysis Workflow
- Rule-based Speaker Identification
- Regex-based PII Redaction

---

# Project Structure

```
fitnova-intelligence/

├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   └── seed.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# Installation

## Backend

Navigate to the backend directory

```bash
cd backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory and add the following variables:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=whisper-large-v3
HF_TOKEN=your_huggingface_token
```

Initialize the database

```bash
python seed.py
```

Start the backend

```bash
uvicorn app.main:app --reload
```

---

## Frontend

Navigate to frontend

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Run the application

```bash
npm run dev
```

---

# Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | API key used for Groq services. |
| `GROQ_MODEL` | Groq Whisper model used for speech transcription. |
| `HF_TOKEN` | Hugging Face access token used by the speaker identification component. |

---

# End-to-End Workflow

The application processes every uploaded call through the following pipeline:

1. Upload an audio recording.
2. Generate transcription using Groq Whisper Large v3.
3. Assign Advisor and Customer speaker labels.
4. Redact Personally Identifiable Information (PII).
5. Analyze the conversation using the AI workflow.
6. Generate sales quality scores.
7. Detect and flag compliance issues.
8. Generate an AI summary.
9. Generate recommendations.
10. Store all processed data in SQLite.
11. Display the results through the dashboard.

---

# What is Real vs Production-Ready

## Implemented & Production-Ready

The following components are fully implemented and production-ready:

- Audio upload and secure streaming playback via HTML5 audio interface
- FastAPI backend APIs (including direct audio streaming endpoints)
- Speech transcription using Groq Whisper Large v3
- Real Speaker Diarization powered by Pyannote.audio (v3.1) with overlap-based timestamp alignment
- Heuristic mapping of diarized speaker tracks to Advisor and Customer roles
- PII redaction (email, phone numbers, cards, UPI IDs)
- AI-powered analysis workflow (evaluating discovery, rapport, compliance, objection handling)
- Sales quality scoring with customized prompts and sentiment analysis
- Compliance issue detection and warning flags
- AI-generated executive summary and actionable recommendations
- SQLite database storage
- Interactive React dashboard with audio playback and messaging-style timeline UI
- Deployment configurations for Render and Vercel

- AI evaluation is prompt-driven using an LLM with predefined scoring criteria and business rules.
- The project is intended as a working prototype demonstrating the complete end-to-end workflow rather than a production-ready sales intelligence platform.

---

# Design Decisions

The project was designed to demonstrate an end-to-end AI sales call intelligence pipeline while keeping the architecture simple, maintainable, and easy to deploy.

### FastAPI

Chosen for its performance, simplicity, and automatic API documentation.

### React + Vite

Used to build a responsive and modern user interface with fast development and build times.

### Groq Whisper Large v3

Used for accurate speech transcription without requiring heavy local inference.

### SQLite

Chosen because it is lightweight, requires no external database server, and simplifies deployment.

### Speaker Identification

A lightweight heuristic-based approach is used to assign Advisor and Customer labels, allowing the prototype to demonstrate the overall processing pipeline without relying on heavy diarization models.

### LangGraph Workflow

The AI analysis engine follows a structured workflow that evaluates conversations, generates scores, detects issues, and produces recommendations.

---

# Trade-offs

To keep the project lightweight and suitable for an internship prototype, several practical trade-offs were made:

- Heuristic speaker identification instead of deep-learning speaker diarization.
- SQLite instead of PostgreSQL.
- Groq Whisper API instead of locally hosted Whisper.
- Prompt-driven AI evaluation instead of a custom-trained machine learning model.

These decisions reduced infrastructure complexity while still demonstrating the complete workflow.

---

# Known Limitations

- Speaker identification is heuristic-based and may not perfectly distinguish speakers in every conversation.
- Poor audio quality can reduce transcription accuracy.
- AI analysis depends on transcription quality.
- The application processes uploaded recordings only and does not support live call streaming.

---

# Future Improvements

Potential future enhancements include:

- Deep-learning speaker diarization using PyAnnote
- Real-time call processing
- Sentiment analysis
- CRM integration
- Team performance analytics
- Multi-language transcription
- Semantic search using vector embeddings
- Authentication and role-based access control

---

# Live Demo

## Frontend

https://fitnova-intelligence-nine.vercel.app/director

## Director Dashboard

https://fitnova-intelligence-nine.vercel.app/director


---

# Author

**Gowtham K**

GitHub:
https://github.com/kgowtham590-spec

---
