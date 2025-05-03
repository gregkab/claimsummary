# Claim Action Intelligence

An intelligent system for extracting action items from insurance claim emails.

## Overview
This application automatically analyzes email threads related to insurance claims, extracts important action items, and organizes them by claim. The system helps claims adjusters stay on top of their tasks and ensure nothing falls through the cracks.

## Features
- Email analysis with GPT-4
- Automatic action item extraction
- Task tracking and management
- Claim-based organization

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React with TailwindCSS
- **Database**: PostgreSQL
- **LLM**: OpenAI GPT-4

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Lock dependencies
pip freeze > requirements.lock.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
# npm will automatically create package-lock.json
npm run dev
```

## Environment Variables
Create a `.env` file in the backend directory with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/claimsummary
OPENAI_API_KEY=your_openai_api_key
FRONTEND_URL=http://localhost:3000
```

## License
MIT 