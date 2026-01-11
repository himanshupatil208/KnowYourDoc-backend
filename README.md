# Know Your Doc – PDF Analyzer API

Know Your Doc is a FastAPI-based backend service that analyzes PDF documents using Google Gemini. 
It extracts text from uploaded PDFs and returns a structured JSON response including a detailed 
summary, document complexity rating, potential risk clauses, key financial figures, and ambiguous terms.

---

## Features
- Upload and analyze PDF documents
- Automatic text extraction from PDFs
- AI-powered document understanding using Gemini
- Structured JSON output for easy frontend integration

---

## Tech Stack
- FastAPI
- Python
- Google Gemini API
- PyPDF2

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the root directory:

```env
API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run the Server
```bash
python main.py
```

Server runs at:
```
http://localhost:8000
```

---

## API Endpoint

### POST `/upload-pdf/`
Uploads a PDF and returns document analysis.

#### Example Request
```bash
curl -X POST http://localhost:8000/upload-pdf/ \
  -F "file=@document.pdf"
```

#### Example Response
```json
{
  "summary": "...",
  "complexity_rating": 7,
  "red_flag_detection": ["..."],
  "figures_extraction": ["..."],
  "loopholes": ["..."]
}
```

---

## Notes
- Works best with text-based PDFs (not scanned images).
- Gemini responses are parsed to extract valid JSON output.

---

