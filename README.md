# FitNova AI Sales Call Intelligence

## Overview

FitNova AI Sales Call Intelligence is an end-to-end AI-powered application that analyzes customer sales calls and provides actionable insights for sales managers.

The system accepts an uploaded call recording, generates a transcript using Groq Whisper, assigns speaker labels, redacts sensitive information, evaluates the conversation using an AI workflow, stores the results in a database, and displays the analysis through an interactive dashboard.

---

## Features

* Upload customer call recordings
* Automatic speech-to-text transcription using Groq Whisper
* Advisor/Customer speaker identification
* Automatic PII redaction (phone numbers, email addresses, card numbers, UPI IDs, etc.)
* AI-powered call analysis
* Sales quality scoring
* Compliance issue detection
* AI-generated call summary
* Recommendations for advisor improvement
* Interactive analytics dashboard

---

## Tech Stack

### Frontend

* React 18
* TypeScript
* Vite
* Tailwind CSS
* Axios
* Recharts
* React Router

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Python

### AI Services

* Groq Whisper Large v3 (Speech Transcription)
* LangGraph-based analysis workflow
* Rule-based speaker diarization
* Regex-based PII redaction

---

## Project Structure

```text
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

## Processing Pipeline

1. Upload an audio file
2. Generate transcription using Groq Whisper
3. Assign Advisor/Customer speaker labels
4. Redact personally identifiable information (PII)
5. Analyze the conversation using the AI workflow
6. Generate quality scores
7. Detect compliance issues
8. Produce a summary and recommendations
9. Store all results in the database
10. Display results in the dashboard

---

## Installation

### Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///fitnova.db
UPLOAD_DIR=uploads
```

Initialize the database:

```bash
python seed.py
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

---

### Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

---

## Deployment

**Frontend**

Hosted on Vercel.

**Backend**

Hosted on Render.

---

## Implemented Components

* Audio upload
* Speech transcription
* Speaker diarization
* PII redaction
* AI analysis workflow
* Call scoring
* Compliance issue detection
* Call summary generation
* Recommendations
* SQLite database storage
* Dashboard visualization

---

## Current Limitations

* Speaker diarization uses a lightweight heuristic approach rather than a dedicated deep-learning diarization model.
* The quality of transcription depends on the uploaded audio.
* Analysis accuracy is influenced by transcription quality.

---

## Future Improvements

* Deep-learning-based speaker diarization
* Real-time call processing
* Sentiment analysis
* CRM integration
* Multi-language support
* Advanced analytics dashboard
* Authentication and role-based access control

---

## Environment Variables

| Variable       | Description                        |
| -------------- | ---------------------------------- |
| `GROQ_API_KEY` | Groq API key for transcription     |
| `DATABASE_URL` | SQLite database connection         |
| `UPLOAD_DIR`   | Directory for uploaded audio files |

---

## Author

**Gowtham K**

GitHub: https://github.com/kgowtham590-spec

---

## License

This project was developed as part of an AI Engineering internship assignment for evaluation and educational purposes.
